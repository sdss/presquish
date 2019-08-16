import numpy
import math

from wok import wok

class woksphere(wok):

    def __init__(self, curvature=1/8800):
        self.curvature = curvature
        self.radius = 1/self.curvature
        self.radiussqd = self.radius**2

    def sag_rsqd(self, radiussqd):
        return self.radius-math.sqrt(self.radiussqd-radiussqd)

    def sag(self, radius):
        return self.sag_rsqd(radius**2)

    def glomsingularlinearconstrained(self, prevrad, separation3d):
        return prevrad+(math.sqrt((separation3d**2/4-self.radiussqd)*(prevrad**2-self.radiussqd))-separation3d*prevrad/2)*separation3d/self.radiussqd

    def glomsingularunconstrainedmultifunc(self, ax, ay, bx, by, separation3d):
        dx = bx-ax
        dy = by-ay
        rootyguy = math.sqrt(separation3d**2/(dx**2+dy**2)-1/4)
        x0 = (ax+bx)/2+dy*rootyguy
        y0 = (ay+by)/2-dx*rootyguy
        x1 = (ax+bx)/2-dy*rootyguy
        y1 = (ay+by)/2+dx*rootyguy
        return ((x0,y0),(x1,y1))
