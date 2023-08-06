from engpy.lib.transforms.laplace import laplace
from engpy.errors.exceptions import UnacceptableToken
from engpy.misc.gen import getter
#from .various import progressions


class Transforms:
    def __init__(self, trns):
        if not getter(trns, 'name') in ('Expr', 'base'):
            raise UnacceptableToken(f'Transforms Class works with Expr objects not {str(type(trns))[8:-2]} Objects')
        self.trns = trns

    def laplace(self, in_var = 't',out_var = 's'):
        return laplace(self.trns, in_var,out_var)

    def z_trn(self):
        
        pass
    def __repr__(self):
        return f'Transforms({self.trns})'
