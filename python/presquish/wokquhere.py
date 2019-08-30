import numpy
import math

from .wok import wok

class wokquhere(wok):

    def __init__(self, curvature=1/8800, quadraticconst=0.0000012336):
        wok.__init__(self)
        self.curvature = curvature
        self.radius = 1/self.curvature
        self.radiussqd = self.radius**2
        self.quadconst = quadraticconst

    def sag_rsqd(self, radiussqd):
        return self.radius-math.sqrt(self.radiussqd-radiussqd)+self.quadconst*radiussqd

    def sag(self, radius):
        return sag_rsqd(radius**2)

    def glomsingularlinearconstrained(self, prevrad, separation3d):
        return prevrad+separation3d

    def glomsingularunconstrainedmultifunc(self, ax, ay, bx, by, separation3d):
        sepsqd = separation3d**2
        sepqqd = sepsqd**2
        dx = ax-bx
        dy = ay-by