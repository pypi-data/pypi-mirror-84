class Measurement:
    def __init__(self, val, unc):
        self.val = val
        self.unc = unc
    def __add__(self, m2):
        val = self.val + m2.val
        unc = norm(self.unc, m2.unc)
        return Measurement(val, unc)
    def __sub__(self, m2):
        val = self.val - m2.val
        unc = norm(self.unc, m2.unc)
        return Measurement(val, unc)
    def __mul__(self, m2):
        if isinstance(m2, Measurement):
            val = self.val*m2.val
            unc = val*norm(self.unc/self.val, m2.unc/m2.val)
            return Measurement(val, unc)
        #Otherwise, it's a scalar
        else:
            return Measurement(self.val*m2, self.unc*m2)
    def __truediv__(self, m2):
        if isinstance(m2, Measurement):
            val = self.val/m2.val
            unc = val*norm(self.unc/self.val, m2.unc/m2.val)
            return Measurement(val, unc)
        else:
            return Measurement(self.val/m2, self.unc/m2)
    def __pow__(self, exp):
        return Measurement(self.val**exp, exp*(self.val)**(exp-1)*self.unc)
    def __str__(self):
        #TODO: improve this printing
        #TODO: Figure out how to use localization(E.g. US vs European notation, etc)
        return f"{self.val:.3f} \\pm {self.unc:.3f}"

def norm(*x):
    return (sum([i**2 for i in x]))**0.5