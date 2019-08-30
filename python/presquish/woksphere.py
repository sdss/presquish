import numpy
import math

from wok import wok

class woksphere(wok):

    def __init__(self, curvature=1/8800):
        wok.__init__(self)
        self.curvature = curvature
        self.radius = 1/self.curvature
        self.radiussqd = self.radius**2

    def sag_rsqd(self, radiussqd):
        if self.radiussqd-radiussqd<0:
            return 0
        else:
            return self.radius-math.sqrt(self.radiussqd-radiussqd)

    def sag(self, radius):
        return self.sag_rsqd(radius**2)

    def glomsingularlinearconstrained(self, prevrad, separation3d):
        return prevrad+(math.sqrt((separation3d**2/4-self.radiussqd)*(prevrad**2-self.radiussqd))-separation3d*prevrad/2)*separation3d/self.radiussqd

    def glomsingularunconstrainedmultifunc(self, ax, ay, bx, by, separation3d):
        sepsqd = separation3d**2
        sepqqd = sepsqd**2
        dx = bx-ax
        dy = by-ay
        rootyboy = math.sqrt(sepsqd/(dx**2+dy**2)-1/4)
        s = 1
        if bx*ay>ax*by:
            s = -1
        startptx = (ax+bx)/2+s*dy*rootyboy
        startpty = (ay+by)/2-s*dx*rootyboy
        angle = math.atan2(startpty-ay,startptx-ax)
        minangle = angle
        maxangle = angle
        

w = woksphere()
grid = w.squishedgrid_full(10,20.002)
import matplotlib.pyplot as p
fig,ax = p.subplots()
ax.scatter(grid[0::2],grid[1::2])
p.show()
