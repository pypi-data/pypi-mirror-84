from engpy.tools.exprs import Expr
from engpy.misc.assist import deepcopy
from engpy.errors.exceptions import *
from engpy.misc.gen import getter
from engpy.misc.miscs import num


class base:

    def __new__(cls, expr = '',nth = 'n', l_bound = 1, u_bound = 100, step = 1, inv = [], **kwargs):
        self = super(base, cls).__new__(cls)
        self.expr =  Expr(expr)
        self.nth = nth
        self.u_bound = u_bound
        self.l_bound = l_bound
        self.inv = [pts for pts in inv if not pts in range(self.l_bound, self.u_bound, self.step)]
        self.step = step
        return self

    def __str__(self):
        return self.expr.cal({self.nth : 'n'}).__str__() if self.nth != 'n' else str(self.expr)
    
    def __iter__(self):
        self.nxt = self.nextseq()
        return self
    
    def __len__(self):
        if self.u_bound == 'n':
            raise InvalidAttribute(f'Infinite Series/Progressions has no length')
        return (self.u_bound - self.l_bound + 1 - len(self.inv))//self.step

    
    
    def len(self, value = ''):
            return [self[i] for i in range(self.l_bound, self.l_bound + value if value else self.u_bound)]
        
    def __next__(self):
        return next(self.nxt)

    def nextseq(self):
        for i in range(self.l_bound,self.u_bound+1, self.step):
            yield self.expr.cal({self.nth: i})
            
    def valid(self, pt):
        return pt in range(self.l_bound, self.u_bound, self.step)

    def cal_(self,values = '', **kvalues):
        if not values:
            values = {}
        for keys, value in kvalues.items():
            values.update({keys: value})
        new = deepcopy(self)
        new.expr = new.expr.cal(values)
        return new

    @property
    def name(self):
        return 'base'
    
    def cal(self,values = '', **kvalues):
        if not values:
            values = {}
        for keys, value in kvalues.items():
            values.update({keys: value})
        self.expr = self.expr.cal(values)
    
    @property
    def first(self):
        return self[self.l_bound]
    
    @property
    def sec(self):
        return self[self.l_bound+1]
    
    @property
    def third(self):
        return self[self.l_bound + 2]
    
    @property
    def last(self):
        return self[self.u_bound/self.step]

    @property
    def sec_last(self):
        return self[self.u_bound - 1]

    @property
    def third_last(self):
        return self[self.u_bound - 2]

    

    def __getitem__(self,other):
    
        if isinstance(other, slice):
            return [self[i] for i in range(other.start, other.stop, 1 if other.step is None else other.step)]
        other *= self.step
        other = num(other)
        if not isinstance(other,int):
            raise UnacceptableToken(f'Index must be an integer')
        if not self.l_bound <= other <= self.u_bound:# or other % self.step != self.l_bound:
            raise OutOfRange(f'This Sequence is valid in range {self.l_bound} - {self.u_bound}' +  (' in the intervals of {self.step}' if self.step - 1 else ''))
        if other in self.inv:
            raise Void(f'This Sequence is not valid for term {other}')
        
        
        return self.expr.cal({self.nth: num(other)})

    @classmethod
    def form(cls):
        return cls
    
    @property
    def recreate(self):
        return self.form()
    __repr__ = __str__

class Series(base):
    def __str__(self):
        return ' + '.join([f'({terms})' if len(terms) > 1 else f'{terms}' for terms in self.len(3)] +
                          ['...', f'({self.last})' if len(self.last) > 1 else f'{self.last}'])

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
        return 'Series'
    
    
    __repr__ = __str__
        

class AP(Series):
    def __init__(self, expr = '',nth = 'n', l_bound = 1, u_bound = 100, inv = [], **kwargs):
        if not expr or getter(expr,'name') == 'Expr':
            self.expr = Series('a + (n-1)d',nth = 'n', l_bound = 1, u_bound = 100, inv = []).expr
            if getter(expr,'name') == 'Expr':
                self.cal(a = expr[1], d = expr[2] - expr[1])
        if kwargs:
            terms = [self[int(terms[1:])] for terms in kwargs]
            value = [values for terms, values in kwargs.items()]
            for_d = 0 if 'd' in str(terms[0]) else 1
            d = (value[0] - value[1]) / (terms[0] - terms[1]).simp().coeff('d')
            self.cal(d = d, a = -(terms[for_d].cal(d = d) - f'a + {value[for_d]}').simp())

    @property
    def name(self):
        return 'AP'

    @property
    def d(self):
        return (self.sec - self.first).simp()
    
    def sum(self, n = ''):
        if not n:
            n = self.u_bound
        return Expr('(n/2)(2a + (n - 1)d)').cal(n = n, a = self.first, d = self.d)


class GP(Series):
    def __init__(self, expr = '',nth = 'n', l_bound = 1, u_bound = 100, inv = [], **kwargs):
        self.name = 'GP'
        if not expr or getter(expr,'name') == 'Expr':
            self.expr = Series('ar^(n-1)',nth = 'n', l_bound = 1, u_bound = 100, inv = []).expr
            if getter(expr,'name') == 'Expr':
                self.cal(a = expr[1], r = expr[2] / expr[1])
        if kwargs:
            order = [int(terms[1:]) for terms in kwargs]
            value = [values for terms, values in kwargs.items()]
            for_d = 0 if 'r' in str(terms[0]) else 1
            r = (value[1] /value[0]) ** (1/(order[1] - order[0]))
            self.cal(r = r, a = value[for_d]/terms[for_d].cal(r = r).coeff('a'))

    @property
    def name(self):
        return 'GP'
    
    @property
    def r(self):
        return self.sec/self.first
    
    def sum(self, n = ''):
        if not n:
            n = self.u_bound
        return Expr('a/(1 - r)').cal(a = self.first, r = self.r) if n == 'inf' else Expr('a(r^n - 1)/(r - 1)' if self.r > 1 else 'a(1 - r^n)/(1 - r)').cal(n = n, a = self.first, r = self.r)
