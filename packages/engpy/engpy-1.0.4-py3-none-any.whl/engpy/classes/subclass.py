from fractions import Fraction
from copy import copy
class mpairs(dict):

    def __str__(self):
        st = ''
        for count, (keys, values) in enumerate(self.items()):
            st += f'{keys} = {values}'
            if not count + 1 == len(self):
                st += ',\n'
        return st

    def restruct(self):
        self_ = copy(self)
        for keys in self_:
            self[keys] = Fraction(self[keys]).limit_denominator()
    def restructs(self):
        self_ = copy(self)
        for keys in self_:
            self[keys] = str(Fraction(self[keys]).limit_denominator())
    
