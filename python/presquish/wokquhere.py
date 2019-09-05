import math
import numpy

from .wok import wok


class wokquhere(wok):

    def __init__(self, curvature=1/8800, quadraticconst=0.0000012336):
        wok.__init__(self)
        self.curvature = curvature
        self.radius = 1/self.curvature
        self.radiussqd = self.radius**2
        self.quadconst = quadraticconst
        self.tolerance = 0.00001

    def sag_rsqd(self, radiussqd):
        return self.radius-math.sqrt(self.radiussqd-radiussqd)+self.quadconst*radiussqd

    def sag(self, radius):
        return self.sag_rsqd(radius**2)

    def glomsingularlinearconstrained(self, prevrad, separation3d):
        sepsqd = separation3d**2
        prevr = self.sag(prevrad)
        x = prevrad+separation3d
        r = self.sag(x)
        err = (x-prevrad)**2+(r-prevr)**2-sepsqd
        while err>self.tolerance:
            r = self.sag(x)
            dx = err
            x -= dx/100
            err = (x-prevrad)**2+(r-prevr)**2-sepsqd
        return x

    def glomsingularunconstrainedmultifunc(self, ax, ay, bx, by, separation3d):
        sepsqd = separation3d**2
        ar = self.sag_rsqd(ax**2+ay**2)
        br = self.sag_rsqd(bx**2+by**2)
        rootyguy = math.sqrt(sepsqd/((ax-bx)**2+(ay-by)**2)-.25)
        x = (ax+bx)/2+(by-ay)*rootyguy
        y = (ay+by)/2-(bx-ax)*rootyguy
        r = self.sag_rsqd(x**2+y**2)
        aerr = (x-ax)**2+(y-ay)**2+(r-ar)**2-sepsqd
        berr = (x-bx)**2+(y-by)**2+(r-br)**2-sepsqd
        err = max(abs(aerr),abs(berr))
        while err>self.tolerance:
            r = self.sag_rsqd(x**2+y**2)
            recipwok = 1/math.sqrt(self.radiussqd-(x**2+y**2))
            dx = aerr*(x*(1+(r-ar)*(recipwok+2*self.quadconst))-ax)+berr*(x*(1+(r-br)*(recipwok+2*self.quadconst))-bx)
            dy = aerr*(y*(1+(r-ar)*(recipwok+2*self.quadconst))-ay)+berr*(y*(1+(r-br)*(recipwok+2*self.quadconst))-by)
            dx = dx/1000
            dy = dy/1000
            x -= dx
            y -= dy
            aerr = (x-ax)**2+(y-ay)**2+(r-ar)**2-sepsqd
            berr = (x-bx)**2+(y-by)**2+(r-br)**2-sepsqd
            err = max(abs(aerr),abs(berr))
        return ((x,y),(ax+bx-x,ay+by-y))