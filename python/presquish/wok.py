import math

class wok:

    def __init__(self):
        pass

    def sag_rsqd(self, radiussqd):
        return sag(math.sqrt(radiussqd))

    def sag(self, radius):
        return 0

    def squishedgrid_3d(self, layers, separation3d):
        grid2d = self.squishedgrid_full(layers, separation3d)
        grid3d = []
        for i in range(0,len(grid2d),2):
            grid3d.append((grid2d[i],grid2d[i+1],self.sag_rsqd(grid2d[i]**2+grid2d[i+1]**2)))
        return grid3d

    def squishedgrid_full(self, layers, separation3d):
        grid = [0,0]
        layer = [0,0]
        for i in range(1,layers):
            newlayer = self.glomlayer(layer, separation3d)
            grid.extend(newlayer)
            layer = newlayer
        return grid

    def glomlayer(self, prevlayer, separation3d):
        newlayer = []
        newrad = self.glomsingularlinearconstrained(prevlayer[0], separation3d)
        halfnewrad = newrad/2
        halfroot3newrad = math.sqrt(3)*halfnewrad
        sixth = int(len(prevlayer)/6)
        if len(prevlayer)>2:
            newlayer.append(newrad)
            newlayer.append(0)
            for i in range(0,sixth,2):
                ax = prevlayer[i]
                ay = prevlayer[i+1]
                bx = prevlayer[i+2]
                by = prevlayer[i+3]
                x,y = self.glomsingularunconstrained(ax,ay,bx,by,separation3d)
                newlayer.append(x)
                newlayer.append(y)
            newlayer.append(halfnewrad)
            newlayer.append(halfroot3newrad)
            for i in range(sixth,2*sixth,2):
                ax = prevlayer[i]
                ay = prevlayer[i+1]
                bx = prevlayer[i+2]
                by = prevlayer[i+3]
                x,y = self.glomsingularunconstrained(ax,ay,bx,by,separation3d)
                newlayer.append(x)
                newlayer.append(y)
            newlayer.append(-halfnewrad)
            newlayer.append(halfroot3newrad)
            for i in range(2*sixth,3*sixth,2):
                ax = prevlayer[i]
                ay = prevlayer[i+1]
                bx = prevlayer[i+2]
                by = prevlayer[i+3]
                x,y = self.glomsingularunconstrained(ax,ay,bx,by,separation3d)
                newlayer.append(x)
                newlayer.append(y)
            newlayer.append(-newrad)
            newlayer.append(0)
            for i in range(3*sixth,4*sixth,2):
                ax = prevlayer[i]
                ay = prevlayer[i+1]
                bx = prevlayer[i+2]
                by = prevlayer[i+3]
                x,y = self.glomsingularunconstrained(ax,ay,bx,by,separation3d)
                newlayer.append(x)
                newlayer.append(y)
            newlayer.append(-halfnewrad)
            newlayer.append(-halfroot3newrad)
            for i in range(4*sixth,5*sixth,2):
                ax = prevlayer[i]
                ay = prevlayer[i+1]
                bx = prevlayer[i+2]
                by = prevlayer[i+3]
                x,y = self.glomsingularunconstrained(ax,ay,bx,by,separation3d)
                newlayer.append(x)
                newlayer.append(y)
            newlayer.append(halfnewrad)
            newlayer.append(-halfroot3newrad)
            for i in range(5*sixth,6*sixth,2):
                ax = prevlayer[i]
                ay = prevlayer[i+1]
                bx = prevlayer[(i+2)%len(prevlayer)]
                by = prevlayer[(i+3)%len(prevlayer)]
                x,y = self.glomsingularunconstrained(ax,ay,bx,by,separation3d)
                newlayer.append(x)
                newlayer.append(y)
        else:
            newlayer.append(newrad)
            newlayer.append(0)
            newlayer.append(halfnewrad)
            newlayer.append(halfroot3newrad)
            newlayer.append(-halfnewrad)
            newlayer.append(halfroot3newrad)
            newlayer.append(-newrad)
            newlayer.append(0)
            newlayer.append(-halfnewrad)
            newlayer.append(-halfroot3newrad)
            newlayer.append(halfnewrad)
            newlayer.append(-halfroot3newrad)
        return newlayer

    def glomsingularunconstrained(self, ax, ay, bx, by, separation3d, fartherfromzero=True, otherwiseclockwise=False):
        p0,p1 = self.glomsingularunconstrainedmultifunc(ax,ay,bx,by,separation3d)
        x0 = p0[0]
        y0 = p0[1]
        x1 = p1[0]
        y1 = p1[1]
        mag0 = x0**2+y0**2
        mag1 = x1**2+y1**2
        if mag0>mag1:
            return (x0,y0)
        elif mag1>mag0:
            return (x1,y1)
        elif x0*y1<x1*y0: #0th point is in counterclockwise half of plane wrt 1th point
            if otherwiseclockwise:
                return (x1,y1)
            else:
                return (x0,y0)
        else: #0th point is in clockwise half of plane wrt 1th point
            if otherwiseclockwise:
                return (x0,y0)
            else:
                return (x1,y1)

    def glomsingularlinearconstrained(self, prevrad, separation3d):
        return prevrad+separation3d

    def glomsingularunconstrainedmultifunc(self, ax, ay, bx, by, separation3d):
        dx = bx-ax
        dy = by-ay
        rootyguy = math.sqrt(separation3d**2/(dx**2+dy**2)-1/4)
        x0 = (ax+bx)/2+dy*rootyguy
        y0 = (ay+by)/2-dx*rootyguy
        x1 = (ax+bx)/2-dy*rootyguy
        y1 = (ay+by)/2+dx*rootyguy
        return ((x0,y0),(x1,y1))
