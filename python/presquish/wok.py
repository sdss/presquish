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
        grid3d = {}
        for i in grid2d:
            grid3d[i] = (grid2d[i][0],grid2d[i][1],self.sag_rsqd(grid2d[i][0]**2+grid2d[i][1]**2))
        return grid3d

    def squishedgrid_full(self, layers, separation3d):
        grid = {(0,0):(0,0)}
        layeridx = 0
        layer = {(0,0):(0,0)}
        for i in range(1,layers):
            self.glomlayer(grid, layeridx, separation3d)
            layeridx += 1
        return grid

    def glomlayer(self, grid, prevlayeridx, separation3d):
        newrad = self.glomsingularlinearconstrained(grid[(prevlayeridx,0)][0], separation3d)
        idx = 0
        halfnewrad = newrad/2
        halfroot3newrad = math.sqrt(3)*halfnewrad
        for i in range(0,prevlayeridx,1):
            for j in range(0,6,1):
                ax = grid[(prevlayeridx,i+j*prevlayeridx)][0]
                ay = grid[(prevlayeridx,i+j*prevlayeridx)][1]
                bx = grid[(prevlayeridx,(i+j*prevlayeridx+1)%(6*prevlayeridx))][0]
                by = grid[(prevlayeridx,(i+j*prevlayeridx+1)%(6*prevlayeridx))][1]
                x,y = self.glomsingularunconstrained(ax,ay,bx,by,separation3d)
                grid[(prevlayeridx+1,i+1+j*(prevlayeridx+1))] = (x,y)
        grid[(prevlayeridx+1,0)] = (newrad,0)
        grid[(prevlayeridx+1,prevlayeridx+1)] = (halfnewrad,halfroot3newrad)
        grid[(prevlayeridx+1,2*(prevlayeridx+1))] = (-halfnewrad,halfroot3newrad)
        grid[(prevlayeridx+1,3*(prevlayeridx+1))] = (-newrad,0)
        grid[(prevlayeridx+1,4*(prevlayeridx+1))] = (-halfnewrad,-halfroot3newrad)
        grid[(prevlayeridx+1,5*(prevlayeridx+1))] = (halfnewrad,-halfroot3newrad)

    def glomsingularunconstrained(self, ax, ay, bx, by, separation3d):
        pts = self.glomsingularunconstrainedmultifunc(ax,ay,bx,by,separation3d)
        maxmag = None
        maxmagidxs = []
        for i in range(len(pts)):
            mag = pts[i][0]**2+pts[i][1]**2
            if maxmag is None or mag>=maxmag:
                if mag==maxmag:
                    maxmagidxs.append(i)
                else:
                    maxmag = mag
                    maxmagidxs = [i]
        return pts[maxmagidxs[0]]

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
