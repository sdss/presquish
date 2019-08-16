import numpy
import math

import wok

class wokspherabola(wok):

    def __init__(self, curvature=1/8800, quadraticconst=0.0000012336):
        self.curvature = curvature
        self.radius = 1/self.curvature
        self.radiussqd = self.radius**2
        self.quadconst = quadraticconst
        pass

    def sag_rsqd(self, radiussqd):
        return self.radius-math.sqrt(self.radiussqd-radiussqd)+self.quadconst*radiussqd

    def sag(self, radius):
        return sag_rsqd(radius**2)

    def glomsingularlinearconstrained(self, prevrad, separation3d):
    return prevrad+separation3d

    def glomsingularunconstrainedmultifunc(self, ax, ay, bx, by, separation3d):
        dx = bx-ax
        dy = by-ay
        print(dx)
        print(dy)
        rootyguy = math.sqrt(separation3d**2/(dx**2+dy**2)-1/4)
        x0 = (ax+bx)/2+dy*rootyguy
        y0 = (ay+by)/2-dx*rootyguy
        x1 = (ax+bx)/2-dy*rootyguy
        y1 = (ay+by)/2+dx*rootyguy
        return ((x0,y0),(x1,y1))