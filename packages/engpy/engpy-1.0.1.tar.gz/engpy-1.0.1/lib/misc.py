from engpy.lib.SS import series
from engpy.misc.assist import List, getter, join
import  engpy.misc.tables as tables


class interpolate:

    def __init__(self, expr, values, var = None):
        expr = series.Expr(expr) if isinstance(expr,str) else expr
        if not isinstance(expr,list):
            if var is None:
                var = expr.vars[0]
        def p_space(X):
            values = []
            for val in X:
                values.append(val); values.append('')
            del values[-1]
            return values
        data = [p_space(values), p_space(list(expr.tables(values,var = var).values())  if not isinstance(expr,list) else expr)]
        dat = data[-1]
        while True:
            if List(dat).unique:
                break
            for ints in range(len(data[-1])):
                if not isinstance(data[-1][ints], str):
                    start = ints
                    break
            for ints, fig in enumerate(reversed(data[-1])):
                if not isinstance(fig, str):
                    stop = len(data[-1]) - ints
                    break
            temp = [(data[-1][i] - data[-1][i-2]) if isinstance(expr,list) else  (data[-1][i] - data[-1][i-2]).simp() for i in range(start, stop,2) if i > start]
            dat = temp
            dat_ = p_space(temp)
            while len(dat_) != len(data[0]):
                dat_ = [''] + dat_
                if len(dat_) != len(data[0]):
                    dat_ += ['']
            data += [dat_]
        data_table = []; task = 0; _task = 0
        while task != len(data[-1]):
            cols = []
            for items in  data:
                cols.append(items[task])
            task += 1
            data_table.append(cols)
        chart = tables.D2_ord(data_table, edge = None)
        #print(chart)
        self.chart = chart
        self.h = values[1] - values[0]
        self.data_table = data_table
        self.data = data

        

    @property
    def values(self):
        return [value for value in self.data[0] if not isinstance(value, str)]
    
    def get_col(self,col):
        return [value for value in self.data[col - 1] if not isinstance(value, str)]
    
    def GNFD(self, value):
        pre_value = 0
        for count, values in enumerate(self.values):
            if values > value:
                p = (value - pre_value)/self.h
                break
            pre_value = values
        f_vals = {}
        F = series.Expr('f0 + pf1')
        for i in range(2, self.chart.cols - 1):
            s = 'p'
            for d in range(i - 1):
                s += f'(p - {d+1})'
            F += f'(({s})f{i})/{i}!'
            f_vals[f'f{i}'] = self.get_col(i + 2)[count - 1]
        return F.cal(f_vals, p = p, f0 = self.get_col(2)[count - 1],
                     f1 = self.get_col(3)[count - 1])
        
    def GFD(self,value):
        pre_value = 0
        for count, values in enumerate(self.values):
            if values > value:
                p = (value - pre_value)/self.h
                break
            pre_value = values
        f_vals = {}
        F = series.Expr('f0 + pf1')
        for i in range(2,self.chart.cols - 1):
            s = 'p'; m = 0
            for d in range(i -1):
                if m + 1< i:
                    s += f'(p - {d + 1})'
                    m += 1
                if m + 1< i:
                    s += f'(p + {d + 1})'
                    m += 1
            F += f'(({s})f{i})/{i}!'
            f_vals[f'f{i}'] = self.get_col(i + 2)[count + (- 1 if i % 2 else -2) - i + 2]
        return F.cal(f_vals, p = p, f0 = self.get_col(2)[count - 1],
                     f1 = self.get_col(3)[count - 1])

    def GBD(self,value):
        pre_value = 0
        for count, values in enumerate(self.values):
            if values > value:
                p = (value - pre_value)/self.h
                break
            pre_value = values
        f_vals = {}
        F = series.Expr('f0 + pf1')
        for i in range(2,self.chart.cols - 1):
            s = 'p'; m = 0
            for d in range(i -1):
                if m + 1< i:
                    s += f'(p + {d + 1})'
                    m += 1
                if m + 1< i:
                    s += f'(p - {d + 1})'
                    m += 1
                    
            F += f'(({s})f{i})/{i}!'
            f_vals[f'f{i}'] = self.get_col(i + 2)[count - i]
        return F.cal(f_vals, p = p, f0 = self.get_col(2)[count - 1],
                     f1 = self.get_col(3)[count - 2])

    def GNBD(self, value):
        pre_value = dec = 0
        if value > self.values[-1] and value < self.values[-1] + 1:
            value -= 1; dec = 1
        for count, values in enumerate(self.values):
            if values > value:
                p = (value - pre_value)/self.h
                break
            pre_value = values
        value += dec; count += dec
        count = len(self.values) - count - 3
        f_vals = {}
        F = series.Expr('f0 + pf1')
        for i in range(2, self.chart.cols - 1):
            s = 'p'
            for d in range(i - 1):
                s += f'(p + {d+1})'
            F += f'(({s})f{i})/{i}!'
            f_vals[f'f{i}'] = self.get_col(i + 2)[count]
        return F.cal(f_vals, p = p, f0 = self.get_col(2)[count],
                     f1 = self.get_col(3)[count])
    
    def Lagrange(self, value):
        return self.eqn.cal(x = value)
    
    @property
    def eqn(self):
        point_list = []
        f, x = (dict(zip([f'f{i}' for i in range(len(self.values))],self.get_col(2))),
                    dict(zip([f'x{i}' for i in range(len(self.values))],self.values)))
        for c, i in enumerate(range(len(self.values))):
            num = ''; den = ''
            for j in range(len(self.values)):
                if not j - i:
                    continue
                num += f'(x - x{j})'; den += f'(x{c} - x{j})'
            point_list.append(series.Expr(f'(({num})/({den}))f{c}').cal(join(f,x)))
        return sum(point_list).simp()
