from engpy.misc.abilities import numable
from engpy.misc.miscs import num
from engpy.misc.gen import getter
from engpy.misc.vars import greek_map


def laplace(expres, in_var='t', out_var='s'):
    if in_var in greek_map:
        in_var = greek_map[in_var]
    new = expres.recreate
    res = new(''); modifier = {}
    refract = '0'
    if len(out_var) > 1:
        refract = new(out_var)
        out_var = 's'
        
    for expr in expres.struct:
        
        if numable(expr):
            res += f'{expr}/{out_var}'
            continue
        coeff = expr._coeff
        var = expr.expr[coeff][0]
        if len(var) > 1:
            if 'ȩ' in var:
                pows = var.pop('ȩ')
                res += laplace(new({coeff:[var]}), in_var,out_var).cal({f'{out_var}':f'{out_var} - {pows.coeff(in_var)}'})
                continue
            if in_var in var:
                pows = var.pop(in_var)
                if pows > 0:
                    res += (-1)** pows * laplace(new({coeff:[var]}), in_var,out_var).lin_diff(f'{out_var}',pows)
                continue
        var_ = list(var)[0]; pow_ = var[var_]
        if getter(var_,'name') not in (None, 'new'):
            res += coeff * var_.laplace(in_var, out_var)
        elif isinstance(var_, str):
            if var_ == in_var:
                res += coeff * new(f'{pow_}!/{out_var}^({pow_} + 1)')
            elif var_ == 'ȩ' and not isinstance(pow_, int):
                res += coeff * ~new(f'{out_var} - {pow_.coeff(in_var)}')

    return res.unify(True) if isinstance(refract, str) else res.cal(s = refract).unify(True)
