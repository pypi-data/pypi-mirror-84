from engpy.lib.SS import series
from engpy.errors.exceptions import *
from engpy.misc.assist import List
from engpy.misc.gen import getter


class Progression(series.base):
    def members(self, stop = '',  values = '', **kvalues):
        if not stop:
            stop = self.u_bound
        if not values:
            values = {}
        for keys, value in kvalues.items():
            values.update({keys: value})
        return [terms._cal(values) for terms in self]
    
    @property
    def name(self):
        return 'Progression'

    def __mul__(self,other):
        self.expr *= other

    def __add__(self,other):
        print([self,other],'ol')
        return Progressions([self,other])

    def __sub__(self,other):
        return Progressions([self,-1 * other])

class Progressions(Progression):
    def __new__(cls, expr = '',nth = 'n', l_bound = '', u_bound = '', step = 0, inv = [], **kwargs):
        if not type(expr) == list:
            print(expr,'iopoi')
            raise UnacceptableToken
        l_bound = []; u_bound = []; step = []
        for exprs in expr:
            if getter(exprs,'name') in ('Progression', 'Progressions'):
                raise UnacceptableToken
            l_bound.append(exprs.l_bound); u_bound.append(exprs.u_bound)
            step.append(exprs.step)
        if not List(step).unique:
            raise InvalidOperation
        self = super(Progressions, cls).__new__(cls)
        self.expr = expr
        self.l_bound = min(l_bound)
        self.u_bound = max(u_bound)
        self.step = step[0]
        self.name = 'Progressions'

    def __str__(self):
        return ' + '.join(str(expr) for expr in self.expr)

    @classmethod
    def __add__(cls,other):
        return cls(self.expr + (other if isinstance(other,list) else [other]))

    @classmethod
    def __sub__(cls,other):
        return cls(self.expr + [-1 * other_ for other in (other if isinstance(other,list) else [other])])

    def __getitem__(self,other):
        other *= self.step
        other = num(other)
        if isinstance(other, slice):
            return [self[i] for i in range(other.start, other.stop, 1 if other.step is None else other.step)]
        if not isinstance(other,int):
            raise UnacceptableToken(f'Index must be an integer')
        if not self.l_bound <= other <= self.u_bound or other % self.step != self.l_bound:
            raise OutOfRange(f'This Sequence is valid in range {self.l_bound} - {self.u_bound}' +  f' in the intervals of {self.step}' if self.step - 1 else '')
        if [inv.inv for inv in self.expr].count(other) == len(self.expr):
            raise Void(f'This Sequence is not valid for term {other}')
        total = 0
        for seq in self.expr:
            try:
                total += seq[other]
            except Void:
                pass
            except OutofRange:
                pass
        return total if isinstance(total,(int,float,complex)) else total.simp()

    @classmethod
    def form(cls):
        return cls
    
    @property
    def recreate(self):
        return self.form()
    __repr__ = __str__
    

class AP(Progression):
    def __init__(self, expr = ''):
        self.name = 'AP'
        if not expr:
            self.expr = Progression('a + (n-1)d')
            if isinstance(expr,(list,tuple)):
                self.cal(a = expr[0], d = expr[1] - expr[0])

    
class GP(Progression):
    def __init__(self, expr = ''):
        self.name = 'GP'
        if not expr:
            self.expr = Progression('ar^(n-1)')
            if isinstance(expr,(list,tuple)):
                self.cal(a = expr[0], r = expr[1] / expr[0])


