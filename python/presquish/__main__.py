#!/usr/bin/env python
#
# @Author: Adam Mendenhall
# @Date: Aug 30, 2019
# @Filename: __main__.py
# @License: BSD 3-Clause
# @Copyright: Adam Mendenhall


from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import argparse
import os
import sys

from .utils import get_config
from .wok import wok
from .wokquhere import wokquhere

if __name__ == '__main__':
    config = get_config('presquish')
    parser = argparse.ArgumentParser(
        prog=os.path.basename(sys.argv[0]),
        description='Plots a squished grid which is equidistant in 3d wokspace.')

    parser.add_argument('wokshape', type=str, help='\'flat\' or \'sphere\' or \'quhere\'')
    parser.add_argument('nlayers', type=int, help='how many hexagonal layers in the grid (1 is a single dot, 2 is 7 dots...)')
    parser.add_argument('separation', type=float, help='the 3d distance between adjacent dots in wokspace')
    parser.add_argument('-outfile', type=str, help='a filename to output the layout information to (displays with matplotlib if not specified)')
    parser.add_argument('-infile', type=str, help='an existing config to mimick the structure of (not the actual locations)')

    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='sets verbose mode')

    args = parser.parse_args()

    w = None
    if args.wokshape=='quhere':
        if args.verbose:
            print('initializing spherical quadratic wok with radius',config['quherewokparams']['radius'],'and quadratic constant',config['quherewokparams']['quadcontrib'])
        w = wokquhere(1/config['quherewokparams']['radius'], config['quherewokparams']['quadcontrib'])
    elif args.wokshape=='sphere':
        if args.verbose:
            print('initializing spherical wok with radius',config['spherewokparams']['radius'])
        w = wokquhere(1/config['spherewokparams']['radius'], config['spherewokparams']['quadcontrib'])
    elif args.wokshape=='flat':
        if args.verbose:
            print('initializing flat wok')
        w = wok()
    else:
        parser.print_help()

    if w is not None:
        if args.verbose:
            print('computing grid with',args.nlayers,'layers and a distance of',args.separation,'between 3d dots')
        grid = w.squishedgrid_3d(args.nlayers, args.separation)
        if args.outfile is None:
            if args.verbose:
                print('displaying grid')
            import matplotlib.pyplot as pyplot
            fig,ax = pyplot.subplots()
            ax.scatter([grid[i][0] for i in grid],[grid[i][1] for i in grid])
            ax.set_aspect(1)
            pyplot.show()
        else:
            import datetime
            if args.infile is not None:
                if args.verbose:
                    print('reading from',args.infile)
                from .utils import ioutils
                from .utils import opticsmath
                import math
                prevconfig = ioutils.specific_instrument_entries_from_file(args.infile,lambda a:True,[0,1,4])
                posfornaivenegforsmart = 0
                with open(args.infile,'r') as f:
                    for line in f:
                        posfornaivenegforsmart += line.lower().count('row')+line.lower().count('pos')
                        posfornaivenegforsmart -= line.lower().count('xangle')+line.lower().count('layer')
                filteredgrid = {}
                if posfornaivenegforsmart>0:
                    for i in range(0,len(prevconfig),1):
                        row = prevconfig[i][0]
                        pos = prevconfig[i][1]
                        r,a = opticsmath.transform_cart2hex_xy2ra(pos+abs(row)/2-args.nlayers,math.sqrt(3)*row/2)
                        prevconfig[i][0] = int(round(r))
                        prevconfig[i][1] = int(round(max(1,6*r)*a))
                for i in range(0,len(prevconfig),1):
                    if (int(prevconfig[i][0]),int(prevconfig[i][1])) in grid:
                        filteredgrid[(int(prevconfig[i][0]),int(prevconfig[i][1]))] = (grid[(int(prevconfig[i][0]),int(prevconfig[i][1]))],prevconfig[i][2])
                if args.verbose:
                    print('writing grid to',args.outfile)
                with open(args.outfile,'w+') as f:
                    f.write('#\n')
                    f.write('# FPS Robot Array Configuration\n')
                    f.write('#\n')
                    f.write('# '+str(datetime.datetime.now())+'\n')
                    f.write('# Layer: nonnegative, layer 0 is the center with only a single dot, layer 1 has six dots\n')
                    f.write('# Xangle = position in layer, x-axis is 0, increases counterclockwise\n')
                    f.write('# X,Y,Z = X,Y,Z position relative to field center (0,0,0)\n')
                    f.write('#\n')
                    l0 = max(len('# Layer'),max([len(str(i[0])) for i in filteredgrid]))+4
                    l1 = max(len('Xangle'),max([len(str(i[1])) for i in filteredgrid]))+4
                    l2 = max(len('X (mm)'),max([len(str(filteredgrid[i][0][0])) for i in filteredgrid]))+4
                    l3 = max(len('Y (mm)'),max([len(str(filteredgrid[i][0][1])) for i in filteredgrid]))+4
                    l4 = max(len('Z (mm)'),max([len(str(filteredgrid[i][0][2])) for i in filteredgrid]))+4
                    l5 = max(len('Assignment'),max([len(str(filteredgrid[i][1])) for i in filteredgrid]))+4
                    f.write('# Layer'.ljust(l0)+'Xangle'.ljust(l1)+'X (mm)'.ljust(l2)+'Y (mm)'.ljust(l3)+'Z (mm)'.ljust(l4)+'Assignment'.ljust(l5)+'\n')
                    for i in filteredgrid:
                        f.write(str(i[0]).ljust(l0)+str(i[1]).ljust(l1)+str(filteredgrid[i][0][0]).ljust(l2)+str(filteredgrid[i][0][1]).ljust(l3)+str(filteredgrid[i][0][2]).ljust(l4)+str(filteredgrid[i][1]).ljust(l5)+'\n')
            else:
                if args.verbose:
                    print('writing grid to',args.outfile)
                with open(args.outfile,'w+') as f:
                    f.write('#\n')
                    f.write('# FPS Robot Array Configuration\n')
                    f.write('#\n')
                    f.write('# '+str(datetime.datetime.now())+'\n')
                    f.write('# Layer: nonnegative, layer 0 is the center with only a single dot, layer 1 has six dots\n')
                    f.write('# Xangle = position in layer, x-axis is 0, increases counterclockwise\n')
                    f.write('# X,Y,Z = X,Y,Z position relative to field center (0,0,0)\n')
                    f.write('#\n')
                    l0 = max(len('# Layer'),max([len(str(i[0])) for i in grid]))+4
                    l1 = max(len('Xangle'),max([len(str(i[1])) for i in grid]))+4
                    l2 = max(len('X (mm)'),max([len(str(grid[i][0])) for i in grid]))+4
                    l3 = max(len('Y (mm)'),max([len(str(grid[i][1])) for i in grid]))+4
                    l4 = max(len('Z (mm)'),max([len(str[grid[i][2]]) for i in grid]))+4
                    f.write('# Layer'.ljust(l0)+'Xangle'.ljust(l1)+'X (mm)'.ljust(l2)+'Y (mm)'.ljust(l3)+'Z (mm)'.ljust(l4)+'\n')
                    for i in grid:
                        f.write(str(i[0]).ljust(l0)+str(i[1]).ljust(l1)+str(grid[i][0]).ljust(l2)+str(grid[i][1]).ljust(l3)+str(grid[i][2]).ljust(l4)+'\n')
