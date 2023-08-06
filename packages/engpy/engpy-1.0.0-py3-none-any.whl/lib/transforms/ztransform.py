from engpy.misc.abilities import numable
from engpy.misc.miscs import alnum
from engpy.misc.miscs import num
from engpy.misc.gen import getter

def ztrns(zt, in_var = 'k', out_var = 'z'):
    
    new = zt.recreate
    res = new({}); zt_out = new({})
    for ztes in zt.struct:
        coeff = ztes._coeff;_var = ztes.expr[coeff][0]; var = list(_var)[0]; pow_ = _var[var]
        if len(_var) == 1 and not getter(var,'name') == 'trig' and isinstance(pow_,(int,float)):
            if ztes >> new(f'{coeff}'):
                zt_out += new(f'{coeff}z/(z-1)')
            elif ztes >> new(f'{coeff}{in_var}'):
                zt_out += new(f'{coeff}z/(z-1)^2')
            elif ztes >> new(f'{coeff}{in_var}^2'):
                zt_out += new(f'{coeff}z(z+1)/(z-1)^3')
            elif ztes >> new(f'{coeff}{in_var}^3'):
                zt_out += new(f'{coeff}z(z^2+4z+1)/(z-1)^4')
            elif var == in_var and isinstance(pow_, int):
                zt_out += (-1)**pow_ * coeff *new(f'{out_var}/({out_var} - 1)').lin_diff(out_var,pow_)
            elif ztes >> new(f'{coeff}{in_var}'):
                zt_out += new(f'{coeff}z/(z-1)^2')
            elif in_var in str(pow_):
                 zt_out += new(f'{coeff}z/(z-{var}^({pow_.coeff(in_var)}))')
                 

        elif getter(var, 'name') == 'trig':
            zt_out += coeff * var.ztransform(in_var, out_var)
        elif len(_var) == 2:
            in_var_cont = [exprs for exprs in _var if not isinstance(exprs,str)]
            in_var_const = [exprs for exprs in _var if in_var in exprs]
            if in_var_const and in_var_cont and in_var_const[0] == in_var:
                zt_out += (-1)**(_var[in_var_const[0]]) * in_var_cont[0].lin_diff(out_var,
                                                       _var[in_var_const[0]])
                continue
            else:
                in_var_cont = [exprs for exprs in _var if isinstance(exprs,str) and not exprs == in_var]
                if in_var_const and in_var_cont and in_var_const[0] == in_var:
                    if _var[in_var_cont[0]] == 'k':
                        zt_out += (-1)**(_var[in_var_const[0]]) * ztrns(new(f'{in_var_cont[0]}^{_var[in_var_cont[0]]}'), in_var, out_var).lin_diff(out_var,
                                                       _var[in_var_const[0]])
                        continue
            in_var_cont = [exprs for exprs in _var.struct if in_var in str(exprs)]
            in_var_const = alnum([exprs for exprs in _var if not in_var in exprs][0])
            if in_var_cont:
                ztrans_ = ztrns(new(f'{in_var_cont}^{pow_}'),in_var, out_var)
            if  not '-' in str(in_var_const):
                zt_out +=  (new(f'z^{in_var_const}')* ztrans_ - sum([new(f'{in_var_cont}^{pow_}').cal({in_var: i})* new(f'z^{in_var_const-i}') for i in range(in_var_const)]))
            elif '-' in str(in_var_const):
                zt_out += new(f'z^{in_var_const}') * ztrans_
            
        elif len(pow_) == 2:
            in_var_cont = [exprs for exprs in pow_.struct if in_var in str(exprs)]
            in_var_const = alnum([exprs for exprs in pow_ if not in_var in str(exprs)][0])
            if in_var_cont:
                ztrans_ = ztrns(new({1:[{var:alnum(in_var_cont[0])}]}),in_var, out_var)
            if in_var_const > 0:
                zt_out +=  (new(f'z^{in_var_const}')* ztrans_ - sum([new(f'{var}^{in_var_cont[0]}').cal({in_var: i}) * new(f'z^{in_var_const-i}') for i in range(in_var_const)]))
                continue
            else:
                zt_out += new(f'z^{in_var_const}') * ztrans_
                continue
    return zt_out
