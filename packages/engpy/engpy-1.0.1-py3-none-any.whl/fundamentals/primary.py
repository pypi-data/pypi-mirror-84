

from engpy.misc import *


class Num:
    def __init__(self,*Num_list):
        if len(Num_list) == 1 and isinstance(Num_list[0],int):
            self.int = Num_list[0]
        elif len(Num_list) > 1:
            self.list = Num_list
        else:
            raise TypeError(str(Num_list) + 'is not an integer')
        
    def is_prime(self,start = 2):
        if isinstance(self.int,int) and not self.int == 1:
            num_range = range(start,self.int)
            for num in num_range:
                if self.int % num == 0:
                    return False
            return True
    def next_prime(self):
        num = self.int+1
        while True:
            while not Num(num).is_prime():
                num +=1
            yield num
            num += 1
        
    def is_even(self):
        if self.int % 2 == 0:
            return True
        return False
    
    def is_odd(self):
        if self.int % 2 == 1:
            return True
        return False

    def is_divisible(self,divisor):
        if not self.int % divisor:
            return True
        return False

    def FirstDivisor(self):
        if isinstance(self.int,int):
            num_range = range(2,self.int+1)
            for num in num_range:
                if self.int % num == 0:
                    return num
        return 1
    def is_perfectsq(self):
        if int(self.int**.5) == self.int**.5:
            return True
        return False
    def prime_factors(self):
        factor_list =[];starter = self.int
        while True:
            divisor = Num(int(starter)).FirstDivisor()
            if not divisor in factor_list: 
                factor_list.append(divisor)
            starter /= divisor
            if starter == 1:
                break
        return Data(factor_list).to_str(', ')
    def in_prime_factors(self):
        factor_list =[];starter = self.int
        while True:
            divisor = Num(int(starter)).FirstDivisor()
            factor_list.append(divisor)
            starter /= divisor
            if int(starter) == 1:
                return Data(factor_list).to_str(' x ')
    def mult_tru(self):
        ans = 1
        try:
            for item in self.list:
                ans *= item
        except AttributeError:
            return self.int
        return ans
    def GCD(self):
        listt = [];factor_list = []
        for item in self.list:
            listt.append(Data(Num(item).in_prime_factors()).count(['x',' ']))
        if listt:
            for item in listt[0]:
                tem = []
                for list in listt:
                    if item in list:
                        tem.append(item)
                if len(tem) == len(listt):
                    tem = []
                    for list in listt:
                        tem.append(list[item])
                    for counting in range(0,min(tem)):
                        factor_list.append(int(item))
            return Num(*factor_list).mult_tru()
    def LCM(self):
        if 0 in self.list:
            return 0
        listt = [];factor_list = [];num_list=[]; tem = []
        listt = [(Data(Num(abs(item)).in_prime_factors()).count(['x',' '])) for item in self.list ]
        if listt:
            for list_ in listt:
                for num in list_:
                    if not num in num_list:
                        num_list.append(num)
            for num in num_list:
                tem = []
                for list_ in listt:
                    try:
                        tem.append(list_[num])
                    except KeyError:
                        tem.append(0)
                for counting in range(0,max(tem)):
                    factor_list.append(int(num))
            return Num(*factor_list).mult_tru()
class Data:
    def __init__(self,typ):
        if isinstance(typ,list):
            self.list = typ
        elif isinstance(typ,str):
            self.str = typ
    def to_str(self,sep = ', '):
        Str ='';counter = 1
        for item in self.list:
            Str += str(item)
            if counter != len(self.list):
                Str += sep
            counter += 1
        return Str
    def count(self,exception=[],split_=' '):
        temp = [];item_list =[]; occurence = []
        for char in self.str.split(split_):
            if not char in temp and not char in exception:
                temp.append(char)
        for item in temp:
            item_list.append(item)
            occurence.append(self.str.count(item))
        return dict(zip(item_list,occurence))
class dic:
    def __init__(self,item,index = None,Error = None,key = '',Limit = True):
        if isinstance(item,dict):
            self.keys = list(item)
            self.values = list(item.values())
            self.Error = Error
        elif index:
            return item[index]
        elif isinstance(item,list):
            self.list = item
            self.key = key
            self.Limit = Limit
        else: self.item = item
        
    def key(self,num):
        if not self.Error:
            return self.values[self.keys.index(num)]
        else:
            try:
                return self.values[self.keys.index(num)]
            except ValueError:
                return num
    def value(self,num):
        if not self.Error:
            return self.keys[self.values.index(num)]
        else:
            try:
                return self.keys[self.values.index(num)]
            except ValueError:
                return num
    def index(self,index):
        return dic(self.item,index = index)
    def search(self,index):
        occurence = 0
        while index < len(self.list):
            if self.list[index] == self.key:
                occurence+=1;index+=1
            elif self.Limit == True and self.list[index] != self.key:
                break
        return occurence

