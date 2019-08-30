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

from .wok import wok
from .wokquhere import wokquhere
from .woksphere import woksphere

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog=os.path.basename(sys.argv[0]),
        description='Plots a squished grid which is equidistant in 3d wokspace.')

    parser.add_argument('wokshape', type=str, help='\'flat\' or \'sphere\' or \'quhere\'')
    parser.add_argument('nlayers', type=int, help='how many hexagonal layers in the grid (1 is a single dot, 2 is 7 dots...)')
    parser.add_argument('separation', type=float, help='the 3d distance between adjacent dots in wokspace')

    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='sets verbose mode')

    args = parser.parse_args()

    w = None
    if args.wokshape=='quhere':
        w = wokquhere()
    elif args.wokshape=='sphere':
        w = woksphere()
    elif args.wokshape=='flat':
        w = wok()
    else:
        parser.print_help()

    if w is not None:
        grid = w.squishedgrid_full(args.nlayers, args.separation)
        import matplotlib.pyplot as pyplot
        fig,ax = pyplot.subplots()
        ax.scatter(grid[0::2],grid[1::2])
        pyplot.show()

    if args.verbose:
        print('here\'s some verbosity for you')