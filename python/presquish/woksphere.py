import numpy
import math

from wok import wok

class woksphere(wok):

    def __init__(self, curvature=1/8800):
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
        dx = ax-bx
        dy = ay-by
        rsqda = ax**2+ay**2
        rsqdb = bx**2+by**2
        saga = self.sag_rsqd(rsqda)
        sagb = self.sag_rsqd(rsqdb)
        dsagsqd = (saga-sagb)**2
        A = (-dx*dy)/(dsagsqd+dx**2)
        B = A**2-(dsagsqd+dy**2)/(dsagsqd+dx**2)
        C = dsagsqd*self.radiussqd/(dsagsqd+dx**2)
        coefs = []
        coefs.append((ax*(2*ay*A-ax)-ay**2*(A**2+B)+self.radiussqd*(A**2+B+1))**2/4-B*(ay**2*A-self.radiussqd*A-ax*ay)**2)
        coefs.append((sepsqd/2-self.radiussqd)*(ax*A+ay)*(ax*(2*ay*A-ax)-ay**2*(A**2+B)+self.radiussqd*(A**2+B+1))-B*(2*self.radiussqd-sepsqd)*(ay**2*A-self.radiussqd*A-ax*ay)*ax)
        coefs.append((sepsqd/2-self.radiussqd)**2*((ax*A+ay)**2-B*ax**2)+(ax*(2*ay*A-ax)-ay**2*(A**2+B)+self.radiussqd*(A**2+B+1))*(sepqqd/4+(C-sepsqd+ax**2+ay**2)*self.radiussqd-ay**2*C)/2-C*(ay**2*A-self.radiussqd*A-ax*ay)**2)
        coefs.append((sepsqd/2-self.radiussqd)*(ax*A+ay)*(sepqqd/4+(C-sepsqd+ax**2+ay**2)*self.radiussqd-ay**2*C)-C*(2*self.radiussqd-sepsqd)*(ay**2*A-self.radiussqd*A-ax*ay)*ax)
        coefs.append(((sepqqd/4+(C-sepsqd+ax**2+ay**2)*self.radiussqd-ay**2*C)/2)**2-(self.radiussqd-sepsqd/2)**2*C*ax**2)
        roots = numpy.roots(coefs)
        possiblesolns = []
        for y in roots:
            if numpy.isreal(y):
                y = numpy.real(y)
                discr = ax**2*(2*self.radiussqd-2*ay*y-sepsqd)**2+4*((rsqda-self.radiussqd)*(y**2-self.radiussqd)-(self.radiussqd-ay*y-sepsqd/2)**2)*(self.radiussqd-ay**2)
                if discr>=0:
                    x = (ax*(2*self.radiussqd-2*ay*y-sepsqd)+math.sqrt(discr))/(2*(self.radiussqd-ay**2))
                    if abs((bx-x)**2+(by-y)**2+(self.sag_rsqd(x**2+y**2)-sagb)**2-sepsqd)<10:
                        possiblesolns.append((x,y))
                discr = ax**2*(2*self.radiussqd-2*ay*y-sepsqd)**2+4*((rsqda-self.radiussqd)*(y**2-self.radiussqd)-(self.radiussqd-ay*y-sepsqd/2)**2)*(self.radiussqd-ay**2)
                if discr>=0:
                    x = (ax*(2*self.radiussqd-2*ay*y-sepsqd)-math.sqrt(discr))/(2*(self.radiussqd-ay**2))
                    if abs((bx-x)**2+(by-y)**2+(self.sag_rsqd(x**2+y**2)-sagb)**2-sepsqd)<10:
                        possiblesolns.append((x,y))
                discr = bx**2*(2*self.radiussqd-2*by*y-sepsqd)**2+4*((rsqdb-self.radiussqd)*(y**2-self.radiussqd)-(self.radiussqd-by*y-sepsqd/2)**2)*(self.radiussqd-by**2)
                if discr>=0:
                    x = (bx*(2*self.radiussqd-2*by*y-sepsqd)+math.sqrt(discr))/(2*(self.radiussqd-by**2))
                    if abs((ax-x)**2+(ay-y)**2+(self.sag_rsqd(x**2+y**2)-saga)**2-sepsqd)<10:
                        possiblesolns.append((x,y))
                discr = bx**2*(2*self.radiussqd-2*by*y-sepsqd)**2+4*((rsqdb-self.radiussqd)*(y**2-self.radiussqd)-(self.radiussqd-by*y-sepsqd/2)**2)*(self.radiussqd-by**2)
                if discr>=0:
                    x = (bx*(2*self.radiussqd-2*by*y-sepsqd)-math.sqrt(discr))/(2*(self.radiussqd-by**2))
                    if abs((ax-x)**2+(ay-y)**2+(self.sag_rsqd(x**2+y**2)-saga)**2-sepsqd)<10:
                        possiblesolns.append((x,y))
        if len(possiblesolns)<1:
            return [(0,0)]
        else:
            return possiblesolns
