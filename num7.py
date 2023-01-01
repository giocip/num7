''' --- SUPREME PRECISION GENERAL PURPOSE ARITHMETIC-LOGIC DECIMAL CLASS --- (SEE DOC AT THE END) ''' 

class Num:
    ''' object self attributes list allowed ''' 
    __slots__ = ('d', 'n', 'n0', 'n1', 'n2', 'L_n0', 'L_n1')
    
    ''' class VARIABLES list ''' 
    pi = '3.141592654'
    e  = '2.718281828'
    
    ''' class METHODS list  ''' 
    
    ''' french financing month mortgage (high precision) '''
    def f_fund_fr(self, i, y) -> 'Num':
        i = Num(i) / 100 
        return (self*i) / (1-(1+i)**-y) / 12 #
    
    ''' french financing month mortgage (high speed) '''
    def f_fund_IEEE754(S, i, y) -> float:
        i = i / 100 
        return (S*i) / (1-(1+i)**-y) / 12
    
    ''' percentage performance value (direct ratio) '''
    def f_perf(self, sob) -> 'Num':
        sob = Num(sob) #allowing float string as: '2.3'
        return (-self + sob) / self * 100
    
    ''' percentage and relative magnitude order time performance value (inverse ratio) '''
    def f_perf_time(self, sob) -> tuple:
        sob = Num(sob) #allowing float string as: '2.3'
        self= Num(self)
        R = ((self - sob) / sob * 100)
        return R, -sob/self+1 if sob>self else self/sob-1 # tuple
    
    ''' add or sub a percentage value to a base price ''' 
    def f_price_over(self, t = 22) -> 'Num':
        t = Num(t) #allowing float string as: '2.3'
        self += self * t / 100
        return self
    
    ''' spin off percentage tax value from a base price ''' 
    def f_price_spinoff(self, t = 22) -> 'Num':
        t = Num(t) #allowing float string as: '2.3'
        return self / ((100+t) / 100)
    
    ''' read a number strings column from disk ''' 
    def f_fileread(filename = 'nums.txt') -> list:
        FILE = [ls for line in open(filename, 'r') if (ls:=line.strip())]
        cart = [Num(str(N)) if '.' in N else Num(str(N)+'.0') for N in FILE]
        return cart #list
    
    ''' write a number strings column from disk ''' 
    def f_filewrite(L, filename = 'nums.txt') -> None:
        lines = [f'{str(i)}\n' for i in L]
        with open(filename, 'a') as FILE:
            FILE.writelines(lines)
        return None

    ''' return Num string '''
    def str(self) -> str:
        return self.__str__()

    ''' return Num representation string '''
    def repr(self) -> str:
        return self.__repr__()
    
    ''' is_numstr to check numeric string validation '''
    def is_numstr(n) -> bool:
        if type(n) != str:
            return False      
        if 'E' in n.upper():            
            n = Num.exp2num(n)
        nv = n.split('.')
        if len(nv) != 2 or not (type(int(nv[0])) == int and nv[1].isnumeric()): 
            return False            
        n0 = nv[0].strip().replace('_', ''); L_n0 = len(n0) #clear space, '_'     
        n1 = nv[1]                         ; L_n1 = len(n1)         
        if  n0[0] == '-':  #negative
            n2 = '-'; n0 = n0[1:]  
        elif n0[0] == '+': #positive
            n2 = '+'; n0 = n0[1:]
        else:
            n2 = '' #positive
        if L_n0 > 1:
            n0 = n0.lstrip('0') #clear LEFT  zeros
            if not len(n0): #if ''
                n0 = '0'
        if L_n1 > 1:
            n1 = n1.rstrip('0') #clear RIGTH zeros
            if not len(n1): #if ''
                n1 = '0'                
        n = n2 + n0 + '.' + n1         #set all number cleaned                 
        if n0 == '0' and n1 == '0': # zero get not any sign == BE CAREFUL!
            if n2 == '-' or n[0] == '+':
                return False 
        return True   

    ''' is_numint checks if integer num '''
    def is_numint(self) -> bool:
        if self.n1 == '0':
            return True
        return False

    ''' is_numfloat checks if floating point num '''
    def is_numfloat(self) -> bool:
        if self.n1 != '0':
            return True
        return False

    ''' is_numeven checks if even num '''
    def is_numeven(self) -> bool:
        if self.is_numint():
            if self % 2:
                return False
            return True
        raise ValueError(F"Num.is_numeven => Num, must be integer value: {self}")
    
    ''' is_numodd checks if odd num '''
    def is_numodd(self) -> bool:
        if self.is_numint():
            if self % 2:
                return True
            return False
        raise ValueError(F"Num.is_numodd => Num, must be integer value: {self}")
    
    ''' convert a scientific notation number to string numeric '''
    def exp2num(s) -> str:
        if type(s) != str:
            raise ValueError(F"Num.exp2num => type not valid: {s}")
        s = s.strip().upper()
        be = s.split('E'); be0 = be[0]; be1 = be[1]
        if len(be) > 2:
            raise ValueError(F"Num.exp2num => scientific notation not valid: {s}")    
        try:
            float(be0); float(be1)
        except:
            raise ValueError(F"Num.exp2num => scientific notation not valid: {s}")
        if be1 == '-0' or be1 == '+0':
            raise ValueError(F"Num.exp2num => zero can not be signed: {s}")    
        POS = False if '-' in be0 else True
        EXP = int(be1);
        bf = be[0].split('.');
        size = len(bf)
        if size != 1:
            bf0 = bf[0]; bf1 = bf[1]
            bf0 = '-' + bf0[1:].lstrip('0') if '-' in bf0 else bf0
            bf0 = ''  + bf0[1:].lstrip('0') if '+' in bf0 else bf0
        else:
            bf0 = be0[1:].lstrip('0') if '+' in be[0] else be[0]
            bf0 = '-' + be0[1:].lstrip('0') if '-' in be[0] else bf0
        L_bf0 = len(bf0) #base length
        if EXP >= 0:
            if POS: #positive integer base
                if size == 1: 
                    return bf0 + EXP*'0' + '.0' #'2e3'
                #size == 2 floating point base                
                L_bf1 = len(bf[1]) #base decs length
                r = bf0 + bf1 + (EXP-L_bf1)*'0'
                DOT = 1 if (EXP-L_bf1) < 0 else 0
                s_CHECK = r[0:L_bf0+EXP] + '.'*DOT + r[L_bf0+EXP:]
                if '.' in s_CHECK:
                    return s_CHECK #'2.3456e3'  
                return s_CHECK + '.0' #'2.3e3'
            #negative integer base
            be0 = be0[0]+'0'+be0[1:].lstrip('0')
            if size == 1: #negative integer base
                return be0 + EXP*'0' + '.0' #'-2e3' #'-1123e2'
            #size == 2 floating point base
            L_bf1 = len(bf[1]) #base decs length
            r = bf[0] + bf[1] + (EXP-L_bf1)*'0'
            DOT = 1 if (EXP-L_bf1) < 0 else 0
            s_CHECK = r[0:L_bf0+EXP] + '.'*DOT + r[L_bf0+EXP:]
            if '.' in s_CHECK:
                return s_CHECK    #'-1.123e2'   
            return s_CHECK + '.0' #'-1.123e3' 
        #EXP < 0
        DOT = L_bf0+EXP; #clear zero on positives only
        if POS: #POS > 0:
            if DOT > 0:
                if size != 1:
                    return bf0[0:DOT] + '.' + bf[0][EXP:] + bf[1] 
                return bf0[0:DOT] + '.' + bf0[DOT:] #'224422e-4'  
            if size != 1:
                return '0.' + (-DOT)*'0' + bf0 + bf1 #'112.3e-13'    
            return '0.' + (-DOT)*'0' + bf0 #'2e-3'
        #POS=false base < 0
        DOT -= 1; L_bf0 -= 1
        if size == 1: #negative integer base
            if DOT > 0:
                return be0[0:EXP] + '.' + be0[EXP:]  #'-22e-1'
            s_TEST = be0[1:]
            return '-0.' + (-DOT)*'0' + s_TEST #'-2522e-4' '-2522e-5'
        #size == 2 floating point base
        if DOT > 0:
            return bf[0][0:EXP] + '.' + bf[0][EXP:] + bf[1]  #'-112.9e-2'
        return '-0.' + (-DOT)*'0' + bf[0][1:] + bf[1] #'-112.9e-3'

    ''' float to IEEE754 conversion '''
    def ieee754(self) -> str: #
        return f'{float(self):.80f}'.rstrip('0')

    ''' float to Num conversion '''
    def float2num(f) -> 'Num':
        return Num(str(f)) 

    ''' float to Num list conversion '''
    def float2num_list(L: list) -> list:
        return [Num((i) if type(i)==int else str(i)) for i in L]
    
    ''' convert a Num object to scientific notation string '''
    def num2exp(ob) -> str:
        if type(ob) != Num:
            raise ValueError(F"Num.num2exp => type not valid: {ob}")
        if ob.n1 == '0': #EXP >= 0
            n0 = ob.n0
            i = len(n0)-1
            e = 0 #s = ''; e = 0
            while i:  #while i >= 0:
                if n0[i] == '0':                    
                    e += 1; i -= 1
                    continue
                break
            if not e:
                return ob.n
            CHECK = n0[0:i+1] + 'e' + str(e) #
            return ob.n2 + CHECK
        if ob.n0 == '0': #EXP < 0
            n1 = ob.n1
            e = 1
            for i in range(len(n1)):
                if n1[i] == '0':
                    e += 1
                    continue
                break
            if not i:
                return ob.n
            CHECK = n1[i:] + 'e-' + str(e+len(n1[i:])-1) #   
            return ob.n2 + CHECK        
        return ob.n
    
    ''' Num integer truncation '''
    def numint(self) -> 'Num':
        return Num(self.n2 + self.n0 + '.0')
    
    ''' Num floating point truncation '''
    def trunc(self, d = 0) -> 'Num':
        m = Num(10)**d
        return Num(int(self * m)) / m

    ''' Num floor rounding '''
    def round_floor(self, d = 0) -> 'Num': #relative value (real number R)
        ''' relative round down: 0.12 => 0.1 -0.12 => -0.2 '''
        if self >= 0: #positives and zero 
            return self.trunc(d)
        #negatives
        e = Num('1.0') / Num('10.0')**d
        if d >= 0:
            t = self.trunc(d) - e; t2 = self - e
            return self if t == t2 else t            
        if e < self:
            return self
        t = self.trunc(d) - e; t2 = self - e
        return self if t == t2 else t            
    
    ''' Num half up rounding '''
    def round(self, d = 2) -> 'Num':
        ''' COMMON STANDARD -relative round_half_ceil: 0.15 => 0.2 -0.15 => -0.1 '''
        return (self + Num('0.5') * Num('10.0')**-d).round_floor(d)
        
    ''' Num half even rounding '''
    def round_bank(self, d = 2) -> 'Num':
        if d < 0:
            d = -d; e = 10**d            
            return (self / Num(e)).round_bank(0) * e
        of = d - self.L_n1
        if of >= 0: 
            return Num(self.n) #0.5 => 0.5 (no round)
        else:
            if not d: #integer rounding (d=0)
                a = int(self.n0); b = int(self.n1[0:1]); c = self.n1[1:].rstrip('0')
                if b > 5: 
                    a += 1
                    return Num(self.n2 + str(a) + '.0') #12.51 => 13.0 integer
                elif b == 5:
                    if a % 2: #odd
                        a += 1
                        return Num(self.n2 + str(a) + '.0') #13.5 => 14.0 integer
                    elif c != '': #even overflow
                        a += 1
                        return Num(self.n2 + str(a) + '.0') #12.51 => 13.0 integer    
                    else: #even
                        if not a:# a == 0
                            return Num('0.0')
                        return Num(self.n2 + str(a) + '.0') #12.5 => 12.0 integer -0.5 => 0.0
                else: 
                    if int(self.n0) >= 1: 
                        return Num(self.n2 + str(a) + '.0') #12.3 => 12.0 integer                                     
                    return Num('0.0') #0.3 => 0.0 #Num(self.n2 + '0.0') 
            # floating point rounding (d>0)
            a = int(self.n1[d-1:d]); b = int(self.n1[d:d+1]); c = self.n1[d+1:].rstrip('0')
            if b > 5:
                a += 1; of2 = 1
                if a > 9: #flag carry
                    while a > 9: 
                        b = 0; s = self.n1[d-of2-1:d-of2]
                        if not s:
                            return Num(self.n2 + str(int(self.n0)+1) + '.0') #3.99 => 4.0
                        a = int(s); a += 1; of2 += 1
                    return Num(self.n2 + self.n0 + '.' + self.n1[0:d-of2] + str(a)) #3.095 => 3.1
                return Num(self.n2 + self.n0 + '.' + self.n1[0:d-1] + str(a)) #3.1415 => 3.142
            elif b == 5:
                if a % 2: #odd
                    a += 1; of2 = 1
                    while a > 9: 
                        b = 0; s = self.n1[d-of2-1:d-of2]
                        if not s:
                            return Num(self.n2 + str(int(self.n0)+1) + '.0') #3.95 => 4.0
                        a = int(s); a += 1; of2 += 1
                    return Num(self.n2 + self.n0 + '.' + self.n1[0:d-of2] + str(a)) #3.095 => 3.1
                elif c != '': #even overflow
                    a += 1
                    return Num(self.n2 + self.n0 + '.' + self.n1[0:d-1] + str(a)) #12.51 => 13.0 integer
                else:  
                    if not a:# a == 0
                        return Num('0.0')
                    return Num(self.n2 + self.n0 + '.' + self.n1[0:d-1] + str(a)) #even 5.65 => 5.6 -0.05 => 0.0
            else: 
                try:
                    return Num(self.n2 + self.n0 + '.' + self.n1[0:d-1] + str(a)) #3.1415 => 3.14 #-0.02 => -0.0 ERROR!
                except:
                    return Num('0.0') #-0.02 => 0.0 OK.
    
    ''' Num ceil rounding '''
    def round_ceil(self, d = 0) -> 'Num':
        ''' relative round up: 0.12 => 0.2 -0.12 => -0.1 '''
        if self <= 0: #negatives and zero 
            return self.trunc(d)
        #positives
        e = Num('1.0') / Num('10.0') ** d
        if d <= 0:
            t = self.trunc(d) + e; t2 = self + e
            return self if t == t2 else t            
        if e > self:
            return self
        t = self.trunc(d) + e; t2 = self + e
        return self if t == t2 else t            
                    
    ''' used by sum() '''
    def reduce(itb, init=None, f=lambda x, y: x+y):
        i = iter(itb)
        x = next(i) if init is None else init
        for y in i:
            x = f(Num(x), Num(y))
        return x

    ''' calculator sum method '''
    def sum(*multi_args: tuple) -> 'Num': 
        return Num.reduce(multi_args)

    ''' calculator mean method '''
    def mean(*multi_args: tuple) -> 'Num': 
        return Num.reduce(multi_args)/len(multi_args) #
    
    ''' calculator min method '''
    def min(L: list) -> 'Num': 
        return min([Num(i) for i in L])
    
    ''' calculator max method '''
    def max(L: list) -> 'Num': 
        return max([Num(i) for i in L])

    ''' calculator ith root method '''
    def root_i(n, i = 3, d = 80):
        if not i:
            return('1.0')
        n = Num(n, d); i = Num(i)
        if i.is_numeven() and n.n2:
            raise ValueError(F"Num.root_i => Negative number: {n}")
        if i < 0:
            n = 1/n
            i = -i
        i = int(i)
        sign = '-' if n < 0 else ''
        n = abs(Num(n))
        n = n.str()
        n0, _, n1 = n.partition('.')
        n = n0 + n1    
        W = i * d - len(n1) #set precision    
        n = n + W*'0' if W >= 0 else n[:W] #integer conversion
        z = n = int(n)
        s = z + 1
        while z<s: #Newton's method
            s = z
            try:
                t = (i-1)*s + n//s**(i-1)
            except:
                raise ValueError(F"Num.root_i => d parameter too low: {d}")
            z = t//i
        s = str(s)   
        if d: #floating point conversion with clearing zeros        
            s = '0' * (1 + d - len(s)) + s
            r = (s[:-d] + '.' +s[-d:]).rstrip('0') 
            s = r + '0' if r[-1] == '.' else r
            return Num(sign + s)
        return Num(sign + s + '.0') #integer conversion
    
    ''' calculator square root method '''
    def sqrt(n, d = 80) -> 'Num':
        n = Num(n)
        if n.L_n0 > 80 and d == 80:
            return Num.sqr(n, n.L_n0)
        return Num.sqr(n, d)
    
    ''' square root method => used by sqrt() '''
    def sqr(n, d = 80):
        ''' sqr(n, d = 80) method runs on python3 trying to be more human style
            and so overcoming sqrt() integer arithmetic limits. (math library function)
        '''                                       
        d = abs(int(d))

        if type(n) == int: #only integer square root (not floating point)        
            if n < 0:
                raise ValueError(F"Num.sqr => Negative number: {n}")
            if not n: # zero
                return 0 #
            L = len(str(n))+1 >> 1 #two division to obtain integer root size
            r = 10**L #Newton's method    
            q = n // r
            while r > q:
                r = r+q >> 1 #two division
                q = n // r         
            return r #

        if type(n) == Num: #str
            nv = str(n).split('.')
            if int(nv[0]) < 0:
                raise ValueError(F"Num.sqr => Negative number: {n}")
                   
            n0 = nv[0]; L_n0 = len(n0)         
            n1 = nv[1]; L_n1 = len(n1)         
                        
            if n0 + '.' + n1 == '0.0': # 0.0
                return Num('0.0')

            L_rx = len(str(n0))+1 >> 1 #X2Division - root digit length                       
            L_n1 = len(n1) #floating digit number 
            
            if n0 == '0': # 0 < n < 1
                shift = L_n1+1 >> 1 #X2Division - decimal point position
                ds = d - shift
                if L_n1 % 2: #odd (dispari):
                    op = n1 + '0' + ds*'00'
                else:        #even (pari)
                    op = n1       + ds*'00'
                r1 = str(Num.sqr(int(op), 0))
                r1_len = len(r1)
                if ds > 0:
                    return Num('0.' + (shift-r1_len+ds)*'0' + r1)
                return Num('0.' + ((shift-r1_len)*'0' + r1)[0:d])
            elif n1 == '0':
                root = str(Num.sqr(int(n0 + d * '00'), 0))
                if not d:
                    return Num(root[0:L_rx] + '.0')    
                return Num(root[0:L_rx] + '.' + root[L_rx:])
            else:
                if L_n1 % 2: #odd (dispari)
                    temp = str(Num.sqr(int(n0 + n1 + '0' + (d-1)*'00'), 0))
                    return Num(temp[0:L_rx] + '.' + temp[L_rx:L_rx+d])
                else:        #even (pari)
                    temp = str(Num.sqr(int(n0 + n1 + (d-1)*'00'), 0))
                    return Num(temp[0:L_rx] + '.' + temp[L_rx:L_rx+d])            
        if type(n) == float:
            raise ValueError(F"Num.sqr => 'float', type not valid: {n}")
        else:
            raise ValueError(F"Num.sqr => Type not valid: {n}")

    ''' division between signed integer number '''
    def _divi_(n, div, d=3):
        '''
            It runs the division between signed integer numbers only and the quotient
                is a floating point string of arbitrary precision (default 3 digits).
        '''
        if not div:
            raise Exception('Num._divi_ => ZeroDivisionError: Num division by zero')     
        n = int(n); div = int(div)    
        n_si   = True if n   < 0 else False
        div_si = True if div < 0 else False    
        n = abs(n); div = abs(div); d = abs(int(d))
        q = n // div; s = str(q) + '.'; k = d #result s
        while k > 0:
            r = n % div; n = r * 10; r = n // div; s += str(r); k -= 1     
        if not (n_si or div_si) or n_si and div_si: #positive
            if not d:
                return s + '0'
            return s
        else: #negative
            if not d:
                r = '-' + s + '0'
                if r == '-0.0':
                    return '0.0'
                return r
            return '-' + s

    ''' Num object constructor '''  
    def __init__(self, n, d = 80):
        #VALIDATION n
        if type(n) == int:
            n = str(n) + '.0' # SUFFIX .0 FOR 'int' type        
        if type(n) == float:
            raise ValueError(F"Num.__init__ => float, type not valid: {n}")            
        if type(n) == Num:
            self.d    = n.d
            self.n    = n.n
            self.n0   = n.n0
            self.n1   = n.n1
            self.n2   = n.n2 
            self.L_n0 = n.L_n0
            self.L_n1 = n.L_n1         
            return None
        if type(n) != str:
            raise ValueError(F"Num.__init__ => type not valid: {n}")    
        if 'E' in n.upper():            
            n = Num.exp2num(n)        
        nv = n.split('.')
        if len(nv) != 2 or not (type(int(nv[0])) == int and nv[1].isnumeric()): 
            raise ValueError(F"Num.__init__ => number format not valid: {n}")                   
        self.n0 = nv[0].strip().replace('_', ''); self.L_n0 = len(self.n0) #clear space, '_'     
        self.n1 = nv[1]                         ; self.L_n1 = len(self.n1)         
        if  self.n0[0] == '-':  #negative
            self.n2 = '-'; self.n0 = self.n0[1:]  
        elif self.n0[0] == '+': #positive
            self.n2 = ''; self.n0 = self.n0[1:]
        else:
            self.n2 = '' #positive
        if self.L_n0 > 1:
            self.n0 = self.n0.lstrip('0') #clear LEFT  zeros
            if not len(self.n0): #if ''
                self.n0 = '0'
        if self.L_n1 > 1:
            self.n1 = self.n1.rstrip('0') #clear RIGTH zeros
            if not len(self.n1): #if ''
                self.n1 = '0'                
        self.L_n0 = len(self.n0); self.L_n1 = len(self.n1) #check for new len       
        self.n = self.n2 + self.n0 + '.' + self.n1         #set all number cleaned 
        if self.n0 == '0' and self.n1 == '0': # zero get not any sign == BE CAREFUL!
            if self.n2 == '-' or n[0] == '+':
                raise ValueError(F"Num.__init__ => zero can not be signed: {n}")    
        self.d = d if d > self.L_n1 else self.L_n1 #precision

    ''' not unary operator '''
    def __bool__(self): #
        return False if self.n == '0.0' else True
    
    ''' (built-in abs function) Return the absolute value of a number '''
    def __abs__(self):        
        return Num(self.n if self.n2 == '' else self.n[1:]) 
    
    ''' abs method calculator '''
    def abs(self) -> 'Num':
        return Num(self).__abs__()

    ''' (+) calculator addition method '''
    def add(a, b) -> 'Num':
        return Num(a) + Num(b)
        
    ''' (+) overloading binary plus operator -used by built-in method sum() '''
    def __add__(self, sob): 
        if type(sob) == int or Num.is_numstr(sob):
            sob = Num(sob)
        if type(sob) != Num:
            raise TypeError(F"Num.__add__( => type not valid: {sob}")
        if   self.L_n1 < sob.L_n1:
            x1 = int(self.n2 + self.n0 + self.n1 + (sob.L_n1-self.L_n1)*'0')
            x2 = int(sob.n2 + sob.n0 + sob.n1)
        elif self.L_n1 > sob.L_n1:
            x1 = int(self.n2 + self.n0 + self.n1)
            x2 = int(sob.n2 + sob.n0 + sob.n1 + (self.L_n1-sob.L_n1)*'0')
        else:
            x1 = int(self.n2 + self.n0 + self.n1)
            x2 = int(sob.n2 + sob.n0 + sob.n1)
        x3 = x1+x2
        if not x3: #zero result addition
            return Num('0.0')
        xt = str(x3)
        xt_L = len(xt)
        xt_D = sob.L_n1 if sob.L_n1 > self.L_n1 else self.L_n1
        if x3 < 0: #Negative add
            ze = xt_D-xt_L+1
            if ze >= 0: #-1 < Negative add < 0
                xtr = '-0' + '.' + ze*'0' + xt[1:]
                return Num(xtr)
        else:      #Positive sub
            ze = xt_D-xt_L
            if ze >= 0: #0 < Positive add < 1
                xtr = '0' + '.' + ze*'0' + xt[0:]
                return Num(xtr)
        sre=Num(xt[0:-xt_D] + '.' + xt[-xt_D:])
        return sre #Constructor
    
    ''' increment variable adding method -object modify by self reference '''
    def inc(self, sob = 1):
        telf = self + sob
        self.d    = telf.d
        self.n    = telf.n
        self.n0   = telf.n0
        self.n1   = telf.n1
        self.n2   = telf.n2 
        self.L_n0 = telf.L_n0
        self.L_n1 = telf.L_n1         
        return self
    
    ''' increment variable multiplying method -object modify by self reference '''
    def incmul(self, sob = 10):
        telf = self * sob
        self.d    = telf.d
        self.n    = telf.n
        self.n0   = telf.n0
        self.n1   = telf.n1
        self.n2   = telf.n2 
        self.L_n0 = telf.L_n0
        self.L_n1 = telf.L_n1         
        return self
    
    ''' decrement variable subtracting method -object modify by self reference '''
    def dec(self, sob = 1):
        telf = self - sob
        self.d    = telf.d
        self.n    = telf.n
        self.n0   = telf.n0
        self.n1   = telf.n1
        self.n2   = telf.n2 
        self.L_n0 = telf.L_n0
        self.L_n1 = telf.L_n1         
        return self
    
    ''' decrement variable dividing method -object modify by self reference '''
    def decdiv(self, sob = 10):
        telf = self / sob
        self.d    = telf.d
        self.n    = telf.n
        self.n0   = telf.n0
        self.n1   = telf.n1
        self.n2   = telf.n2 
        self.L_n0 = telf.L_n0
        self.L_n1 = telf.L_n1         
        return self
    
    ''' clear variable '''
    def clear(self):
        telf = self
        self.d    = telf.d
        self.n    = '0.0'
        self.n0   = '0'
        self.n1   = '0'
        self.n2   = ''
        self.L_n0 = 1
        self.L_n1 = 1         
        return self
        
    ''' (+) swap operands binary plus operator -mandatory by built-in method sum() '''
    __radd__ = __add__ 
    
    ''' (-) calculator subtract method '''
    def sub(a, b) -> 'Num':
        return Num(a) - Num(b)

    ''' (-) overloading binary minus operator '''
    def __sub__(self, sob): 
        if type(sob) == int or Num.is_numstr(sob):
            sob = Num(sob)
        if type(sob) != Num:
            raise TypeError(F"Num.__sub__ => type not valid: {sob}")
        if   self.L_n1 < sob.L_n1:
            x1 = int(self.n2 + self.n0 + self.n1 + (sob.L_n1-self.L_n1)*'0')
            x2 = int(sob.n2 + sob.n0 + sob.n1)
        elif self.L_n1 > sob.L_n1:
            x1 = int(self.n2 + self.n0 + self.n1)
            x2 = int(sob.n2 + sob.n0 + sob.n1 + (self.L_n1-sob.L_n1)*'0')
        else:
            x1 = int(self.n2 + self.n0 + self.n1)
            x2 = int(sob.n2 + sob.n0 + sob.n1)
        x3 = x1-x2
        if not x3: #zero result subtraction
            return Num('0.0')
        xt = str(x3)
        xt_L = len(xt)
        xt_D = sob.L_n1 if sob.L_n1 > self.L_n1 else self.L_n1
        if x3 < 0: #Negative sub
            ze = xt_D-xt_L+1
            if ze >= 0: #-1 < Negative sub < 0
                xtr = '-0' + '.' + ze*'0' + xt[1:]
                return Num(xtr)
        else:      #Positive sub
            ze = xt_D-xt_L
            if ze >= 0: #0 < Positive sub < 1
                xtr = '0' + '.' + ze*'0' + xt[0:]
                return Num(xtr)
        sre=Num(xt[0:-xt_D] + '.' + xt[-xt_D:])
        return sre #Constructor
    
    ''' (-) swap operands binary minus operator '''
    def __rsub__(self, sob): 
        return Num(sob).__sub__(self)
            
    ''' (*) calculator multiplication method '''
    def mul(a, b) -> 'Num':
        return Num(a) * Num(b)
    
    ''' (*) overloading binary multiply operator '''
    def __mul__(self, sob): 
        if type(sob) == int or Num.is_numstr(sob):
            sob = Num(sob)
        if type(sob) != Num:
            raise TypeError(F"Num.__mul__ => type not valid: {sob}")
        x1 = int(self.n2 + self.n0 + self.n1); x2 = int(sob.n2 + sob.n0 + sob.n1)
        x3 = x1*x2
        if not x3: #multiply with 0
            return Num('0.0')
        xt = str(x3); xt_L = len(xt); xt_D = self.L_n1 + sob.L_n1 
        if x3 < 0: #Negative
            ze = xt_D-xt_L+1
            if ze >= 0:
                return Num('-0' + '.' + ze*'0' + xt[1:])
            return Num(xt[0:-xt_D] + '.' + xt[-xt_D:])
        ze = xt_D-xt_L
        if ze >= 0:
            return Num('0' + '.' + ze*'0' + xt[0:])
        return Num(xt[0:-xt_D] + '.' + xt[-xt_D:])
    
    ''' (<<) left shift binary operator -multiplying for 10 powers '''
    def __lshift__(self, sob):
        return self * 10**Num(sob)
    
    ''' (<<) swap operands left shift binary operator '''
    def __rlshift__(self, sob):
        return Num(sob).__lshift__(self)
        
    ''' (*) swap operands binary multiplication operator '''
    __rmul__ = __mul__ 
    
    ''' (/) calculator division method '''
    def div(a, b) -> 'Num':
        return Num(a) / Num(b)
    
    ''' (/) overloading binary floating point division operator  '''
    def __truediv__(self, sob): 
        if type(sob) == int or Num.is_numstr(sob):
           sob = Num(sob)
        if type(sob) != Num:
            raise TypeError(F"Num.__truediv__ => type not valid: {sob}")
        if self.n == '0.0':
            return Num('0.0')
        if self.L_n1 > sob.L_n1:
            ze = self.L_n1 - sob.L_n1
            x1 = int(self.n2 + self.n0 + self.n1); x2 = int(sob.n2 + sob.n0 + sob.n1 + ze*'0')                 
            x3 = Num._divi_(x1, x2, self.d if self.d > sob.d else sob.d)
        else:
            ze = sob.L_n1 - self.L_n1
            x1 = int(self.n2 + self.n0 + self.n1 + ze*'0'); x2 = int(sob.n2 + sob.n0 + sob.n1)                  
            x3 = Num._divi_(x1, x2, self.d if self.d > sob.d else sob.d)                            
        return Num(x3)

    ''' (/) swap operands floating point division binary operator  '''
    def __rtruediv__(self, sob): 
        return Num(sob).__truediv__(self)
    
    ''' (//) overloading integer division binary operator '''
    def __floordiv__(self, sob): 
        if type(sob) == int or Num.is_numstr(sob):
            sob = Num(sob)
        if type(sob) != Num:
            raise TypeError(F"Num.__floordiv__ => type not valid: {sob}")
        if self.n == '0.0':
            return Num('0.0')
        if self.L_n1 > sob.L_n1:
            ze = self.L_n1 - sob.L_n1
            x1 = int(self.n2 + self.n0 + self.n1); x2 = int(sob.n2 + sob.n0 + sob.n1 + ze*'0')               
            x3 = Num._divi_(x1, x2, 0)
        else:
            ze = sob.L_n1 - self.L_n1
            x1 = int(self.n2 + self.n0 + self.n1 + ze*'0'); x2 = int(sob.n2 + sob.n0 + sob.n1)            
            x3 = Num._divi_(x1, x2, 0)                            
        return Num(x3)
    
    ''' (//) swap operands integer division binary operator '''
    def __rfloordiv__(self, sob): 
        return Num(sob).__floordiv__(self)

    ''' (%) overloading module binary operator (Num floating point division remainder) '''
    def __mod__(self, sob): 
        if type(sob) == int or Num.is_numstr(sob):
            sob = Num(sob)
        if type(sob) != Num:
            raise TypeError(F"Num.__mod__ => type not valid: {sob}")
        if self.n == '0.0':
            return Num('0.0')
        if self.L_n1 > sob.L_n1:
            ze = self.L_n1 - sob.L_n1
            x1 = int(self.n2 + self.n0 + self.n1); x2 = int(sob.n2 + sob.n0 + sob.n1 + ze*'0')                 
            x3 = Num._divi_(x1, x2, 0)
        else:
            ze = sob.L_n1 - self.L_n1
            x1 = int(self.n2 + self.n0 + self.n1 + ze*'0'); x2 = int(sob.n2 + sob.n0 + sob.n1)            
            x3 = Num._divi_(x1, x2, 0)                            
        return self - (Num(x3) * sob)

    ''' (%) swap operands module operator (integer division remainder) '''
    def __rmod__(self, sob): 
        return Num(sob).__mod__(self)

    ''' (// %) calculator divmod return a tuple (self // sob, self % sob) '''
    def divmod(self, sob) -> tuple:    
        Q = Num(self).__floordiv__(Num(sob))
        R = Num(self).__mod__(Num(sob))
        return Q, R

    ''' (divmod built-in method) return a tuple (self // sob, self % sob) '''
    def __divmod__(self, sob):    
        Q = (self).__floordiv__((sob))
        R = (self).__mod__((sob))
        return Q, R

    ''' (divmod built-in method) swap operands '''
    def __rdivmod__(self, sob): 
        return Num(sob).__divmod__(self)
    
    ''' (>>) right shift binary operator -dividing for ten powers '''
    def __rshift__(self, sob):
        sob = Num(sob)
        t = sob + self.L_n1
        self.d = t if t > self.d else self.d
        return self / 10**sob
    
    ''' (>>) swap operands right shift binary operator '''
    def __rrshift__(self, sob):
        return Num(sob).__rshift__(self)
   
                
    ''' (== !=) overloading equal and not equal logic binary operators '''
    def __eq__(self, sob): #== !=
        sob = Num(sob)
        return True if self.n == sob.n else False
    
    ''' (>) overloading greater logic binary operator '''
    def __gt__(self, sob): #>
        sob = Num(sob)
        if int(self.n2+self.n0) > int(sob.n2+sob.n0):
            return True
        if int(self.n2+self.n0) == int(sob.n2+sob.n0):
            d_L1 = self.L_n1 - sob.L_n1
            if d_L1 > 0:
                a = int(self.n2+self.n1); b = int(sob.n2+sob.n1+abs(d_L1)*'0')                
                if a > b:
                    return True
            elif d_L1 < 0:
                a = int(self.n2+self.n1+abs(d_L1)*'0'); b = int(sob.n2+sob.n1)                
                if a > b:
                    return True
            else:
                return True if int(self.n2+self.n1) > int(sob.n2+sob.n1) else False
        return False

    ''' (>=) overloading greater or equal logic binary operator '''
    def __ge__(self, sob): #>=
        return True if self > sob or self == sob else False

    ''' (<) overloading less logic binary operator '''
    def __lt__(self, sob): #<
        return False if self >= sob else True #

    ''' (<=) overloading less or equal logic binary operator '''
    def __le__(self, sob): #<=
        return False if self > sob else True  #
    
    ''' overloading built-in method len() '''
    def __len__(self):
        return len(self.n)
    
    ''' return a tuple with num lengths before and after floating point dot '''
    def len(self) -> tuple:
        return len(self.n0), 0 if len(self.n1) == 1 and self.n1 == '0' else len(self.n1)       
    
    ''' overloading unary operator - '''
    def __neg__(self): #
        return Num(self.n[1:]) if self.n2 == '-' else Num('-' + self.n)
    
    ''' overloading unary operator + '''
    def __pos__(self): #
        return Num(self.n)
    
    ''' (built-in int method) Num to int (truncation) - great loss precision! '''
    def __int__(self): #
        return int(self.n2 + self.n0) 

    ''' (truncation) Num to int method - great loss precision! '''
    def int(self) -> int: #
        return self.__int__()

    ''' Num to float (loss precision!) '''
    def __float__(self): #
        return float(self.n)

    ''' pow method calculator '''
    def pow(self, e) -> 'Num':
        return Num(self).__pow__(Num(e))        
    
    ''' (**) overloading power binary operator and used by built-in function pow() '''
    def __pow__(self, e): # e mandatory,  
        if type(e) != int and type(e) != Num:
            raise ValueError(F"Num.__pow__ => type not valid: {e}")            
        if type(e) == int or type(e) == Num and e.is_numint():            
            if e < 0:
                b = i = Num('1.0') / self #
                e = -e
                while e > 1:
                    b *= i
                    e -= 1
            else:
                b = Num('1.0')
                while e > 0:
                    b *= self #Num(self.n)
                    e -= 1
            return b   
        raise ValueError(F"Num.__pow__ => Num, must be integer value: {e}")
    
    ''' (**) swap operands power binary operator '''
    def __rpow__(self, sob): 
        return Num(sob).__pow__(self)

    ''' built-in function round() '''
    def __round__(self, d = 2):  #   
        return self.round(d)
    
    ''' like math.trunc() function '''
    def __trunc__(self): #
        return self.__int__()
    
    ''' built-in function str() '''
    def __str__(self): #  
        return self.n # self.n

    ''' built-in function repr() '''
    def __repr__(self): #almost like __str__ (obj representation in REPL)
        return str('Num(\'' + self.n + '\')')
    
    def doc():
        return '''        --- SUPREME PRECISION GENERAL PURPOSE ARITHMETIC-LOGIC DECIMAL CLASS DOCUMENTATION ---

        Num is a lightweight floating point numeric class for arbitrary precision results with always supreme precision.        
        
        Easy to use like school math and WITHOUT IEEE754 ISSUES or +0 AND -0 FAILURES, it can be deployed for
        web e-commerce developing, accounting apps and general math programs included financial ones.
        
        HOW TO USE (integer numeric strings (ex. '2.0') MUST BE SUFFIXED WITH .0):                        
        --- CALCULATOR MODE ---           
                           >>> from num7 import Num, Num as calc
                           
        ADDITION:          >>> calc.add('-5.3', '2.1')    # Num('-3.2')
        SUBTRACTION:       >>> calc.sub('-5.3', '2.1')    # Num('-7.4')
        MULTIPLICATION:    >>> calc.mul('-5.3', '2.1')    # Num('-11.13')
        DIVISION:          >>> calc.div('-5.3', '2.1')    # Num('-2.52380952380952380952380952380952380952380952380952380952380952380952380952380952')
        M+:                >>> M = calc('0.0'); M.inc('3.0'); M.inc('3.3'); M.inc('3.7'); print(M) # 10.0
        M-:                >>>                  M.dec('5.0'); M.dec('3.3'); M.dec('1.5'); print(M) # 0.2
        MC:                >>> M.clear(); print(M) # 0.0
        INT   DIV AND REM: >>> calc.divmod('5.0', '3.0')  # (Num('1.0'), Num('2.0')) => tuple 
        FLOAT DIV AND REM: >>> calc.divmod('5.2', '3.1')  # (Num('1.0'), Num('2.1')) => tuple
        POWER:             >>> calc.pow('-5.3', '2.0')    # Num('28.09')
        SQRT:              >>> calc.sqrt('2.0')           # Num('1.41421356237309504880168872420969807856967187537694807317667973799073247846210703')
        ROOT_ith           >>> calc.root_i('1.860867', 3) # Num('1.23')        
        ROUND:             >>> calc.sqrt('2.0').round(2)  # Num('1.41')
        ABSOLUTE VALUE     >>> calc.abs('-3.0')           # Num('3.0')
        SUM:               >>> cart = ['19.32','18.37','15.13']; calc.sum(*cart)          # Num('52.82')
        MEAN:              >>> cart = ['19.32','18.37','15.13']; calc.mean(*cart).round() # Num('17.61')
        MIN:               >>> cart = ['19.32','18.37','15.13']; calc.min(cart)           # Num('15.13')
        MAX:               >>> cart = ['19.32','18.37','15.13']; calc.max(cart)           # Num('19.32')
        EXP:               >>> calc.mul('-5.3e1024', '2.1e1024').num2exp()                # '-1113E2046'
        REPL:              >>> a = calc('0.1'); b = calc('0.2'); print(calc.add(a, b))    # 0.3

        CODING:
            >>> from num7 import Num, Num as calc
        
            (=) assignment:
                >>> a = Num('3.0'); b = Num('5.0'); c = Num('0.0'); #
                >>> print('a =', a, 'b =', b, 'c =', c) # a = 3.0 b = 5.0 c = 0.0
            
            (+) adding:
                >>> R = a+b+c; print(R) # 8.0
                >>> a = Num('0.1'); b = Num('0.2'); c = Num('0.0'); print(a+b+c) # 0.3
                
            (-) subtracting:
                >>> a = Num('0.1'); b = Num('0.2'); c = Num('0.3');
                >>> print(a+b-c) # 0.0
                >>> R = Num('-3.99') - Num('-5.20') - Num('+3.01'); print(R) # -1.8
            
            (*) multiplying:
                >>> Num('-3.99') * Num('-5.20') * Num('+3.01') # -3.99 * (-5.20) * (+3.01 ) = Num('62.45148')    
             
            (/) dividing (80 decimal digits default gets only for division operation):
                >>> Num('3.0') / Num('5.7') # 3 : 5.7 = Num('0.52631578947368421052631578947368421052631578947368421052631578947368421052631578') 
                
                Division precision may be specified as parameter after numeric string as:
                                                                                128 decs
                >>> Num('3.0', 128) / Num('5.7', 128) # 3 : 5.7 = Num('0.52631578947368421052631578947368421052631578947368421052631578947368421052631578947368421052631578947368421052631578947368421052')
            
            (// % operators, divmod python3 built-in function) int division and remainder :
                >>> a = Num('5.0'); b = Num('2.0') #
                >>> Q = a // b; R = a % b; print('Quotient =', Q, 'Remainder =', R) # Quotient = 2.0 Remainder = 1.0
                >>> a = Num('15.0'); b = Num('4.0') #
                >>> Q, R = divmod(a, b); print('Quotient =', Q, 'Remainder =', R)   # Quotient = 3.0 Remainder = 3.0
            
            (divmod python3 built-in function) floating division and remainder:
                >>> a = Num('10.123456789'); b = Num('2.0') #
                >>> Q, R = divmod(a, b); print('Quotient =', Q, 'Remainder =', R)   # Quotient = 5.0 Remainder = 0.123456789
        
            (sqrt) square root function:
                >>> a = Num('123_456_789.1234567890123456789'); root = a.sqrt() # Num('11111.11106611111096998611053449930232404576951925017079015206589094347963821409843324')
                >>> print('result digits number tuple =>', root.len()) # result digits number tuple => (5, 80)
                
            (**) power operator and pow python3 built-in function:
                >>> a = Num('2.22123') ** 64; print(a) # 15204983311631674774944.6514720988866075755417446332131101580789367
                                                         9105748958794491681177995203669698667160837739445605536688871012507
                                                         1945418498486819681408058765704850273804729367340948014205522859407
                                                         6533821958836232769517779825179391210405799994330832050119578417313
                                                         5380826413054938730768027747418766018606636039075568645106645889100
                                                         039914241
                >>> print(a.len()) # (23, 320) digits len tuple
                >>> print(Num(Num.pi))  # 3.141592654
                >>> pow(Num(Num.pi), 8) # Num('9488.531025982131642534428505085353941520356351078169077371202330414440366336')
        
        
            logic (in, not in, is, is not, <, <=, >, >=, !=, ==) and relational operators (and, or, not).
             
             (in):
                >>> L = [Num('0.1'), Num('1.0'), Num('5.5'), Num('-3.0'), Num('-2.9'), Num('-3.0001'), Num('2.2')]
                >>> Num('-3.0001') in L; Num('-3.00001') in L         #True False
             
             (not in):
                >>> Num('-3.0001') not in L; Num('-3.00001') not in L #False True
             
             (is, is not):
                >>> M = calc('0.0'); Num('0.0') is M # False
                >>> M = calc('0.0'); M.inc('0.1') is not M; M # True Num('0.1')
                >>> M; N = M; N.dec('0.1'); N is M; M; N # Num('0.1') True Num('0.0') Num('0.0')
                
             (< <= > >= != ==)
                >>> a = Num('0.0'); b = Num('0.1'); c = Num('-0.2')
                >>> a <  b; a <  c; b <  c #True  False False
                >>> a <= a; a <= c; b <= c #True  False False
                >>> a >  b; a >  c; b >  c #False True  True
                >>> a >= a; a >= c; b >= c #True  True  True
                >>> c == -2*b; a == c + 2*b ; a != a+b+c #True  True  True
                >>> a and b; a or b; not a     # Num('0.0') Num('0.1') True
                >>> True if a and b else False # False
                >>> True if a or  b else False # True
                
             (+ - unary operators)
                >>> Num('+2.5521') # Num('2.5521')
                >>> Num('-3.3321') # Num('-3.3321')
                >>> Num('+2.5521') + Num('-3.3321') # Num('-0.78')

            #variable arithmetics -On a given variable, the following arithmetic methods are available:
                from num7 import Num
                a = Num('10.25');
                print(a)       #10.25
                a.inc()        #increment (default) by one
                print(a)       #11.25
                a.dec(2)       #decrement (optional) 2 units
                print(a)       #9.25
                a.incmul()     #multiply (default) 10 times
                print(a)       #92.5
                a.decdiv(100)  #x100 (optional) division
                print(a)       #0.925
                a.clear()      #a variable set to zero
                print(a)       #0.0

            #EVEN ODD numbering methods:
                from num7 import Num
                a = Num(6); b = Num(3); c = Num('3.14')  
                print(a, 'INTEGER =>', a.is_numint(), 'EVEN =>', a.is_numeven())  
                print(b, 'INTEGER =>', b.is_numint(), 'ODD  =>', b.is_numodd())  
                print(c, 'FLOAT  =>', c.is_numfloat())

        ######################## advanced logic programming snippet ########################
    ### LOOP EXAMPLE >>>        
from num7 import Num, Num as calc
i = Num(0)
while i < Num('1.0'):
    i.inc('0.1') #i += Num('0.1')
    if i <= Num('0.5'):
        continue
    print(i) # 0.6, 0.7, 0.8, 0.9, 1.0
while i:
    i.dec('0.1') #i -= Num('0.1')
    if i >= Num('0.5'):
        continue
    print(i) #0.4 0.3 0.2 0.1 0.0  

    ### ROUNDING AND ACCOUNTING >>>
from num7 import Num, Num as calc
p = Num('11.19')               #PRICE -Toslink cable for soundbar
pd = round(p.f_price_over(-7)) #PRICE DISCOUNTED 7%
d = round(p - pd)              #DISCOUNT
p_noTAX = round(p.f_price_spinoff(22)) #ITEM COST WITHOUT TAX 22%
TAX = round(p - p_noTAX)               #TAX 22%
print(F'price={p} PAYED={pd} discount={d} COST={p_noTAX} TAX={TAX}') #price=11.19 PAYED=10.41 discount=0.78 COST=9.17 TAX=2.02

    ### OUTPUT FORMATTING AND LOCALIZATION >>>
import locale
from num7 import Num
s = locale.setlocale(locale.LC_ALL, "")
print('settings:', s) #settings: Italian_Italy.1252
#calculating banking loan
asset = Num('100_000.0'); rate = Num('6.5'); years = Num('20.0')
monthly_payment = Num.f_fund_fr(asset, rate, years)
print(locale.format_string("%.2f", float(monthly_payment)))   #756,30
print(locale.currency(float(monthly_payment), grouping=True)) #756,30 €

    ### ROUNDING TYPES >>>
from num7 import Num  
### Num floor rounding ###
print('--' * 10 + ' Num floor rounding')  
n = Num(Num.pi)            # 3.141592654  
print(n, n.round_floor(2)) # 3.14  
n = -Num(Num.pi)           #-3.141592654  
print(n, n.round_floor(2)) #-3.15  
n = Num(Num.pi) - 3        # 0.141592654  
print(n, n.round_floor(2)) # 0.14  
n = -Num(Num.pi) + 3       #-0.141592654  
print(n, n.round_floor(2)) #-0.15  

print('--' * 10 + ' Num ceil rounding')  
### Num ceil rounding ###
n = Num(Num.pi)           # 3.141592654  
print(n, n.round_ceil(2)) # 3.15  
n = -Num(Num.pi)          #-3.141592654  
print(n, n.round_ceil(2)) #-3.14  
n = Num(Num.pi) - 3       # 0.141592654  
print(n, n.round_ceil(2)) # 0.15  
n = -Num(Num.pi) + 3      #-0.141592654  
print(n, n.round_ceil(2)) #-0.14  

print('--' * 10 + ' Num standard rounding')  
### Num standard rounding ###
n = Num(Num.pi)      # 3.141592654  
print(n, n.round())  # 3.14  
n = -Num(Num.pi)     #-3.141592654  
print(n, n.round())  #-3.14  
n = Num(Num.pi) - 3  # 0.141592654  
print(n, n.round(4)) # 0.1416  
n = -Num(Num.pi) + 3 #-0.141592654  
print(n, n.round(4)) #-0.1416  

print('--' * 10 + ' Num half to even rounding (statistic, zero symmetric)')  
### Num half even rounding ###
n = Num(Num.pi).round_floor(4)      # 3.1415  
print(n, n.round_bank(3))           # 3.142  
n = -Num(Num.pi).round_floor(4)     #-3.1415  
print(n, n.round_bank(3))           #-3.142  
n = Num(Num.pi).round_floor(8) - 3  # 0.14159265  
print(n, n.round_bank(7))           # 0.1415926  
n = -Num(Num.pi).round_floor(8) + 3 #-0.14159265  
print(n, n.round_bank(7))           #-0.1415926  

    ### PERFORMANCE EVALUATION AND SQUARENESS >>>
#from sys import set_int_max_str_digits #PYTHON 3.11
from num7 import Num, Num as calc
from time import perf_counter
#set_int_max_str_digits(1_000_000) #PYTHON 3.11
digits = 109
tic = perf_counter() # Start Time
a = Num('-1.123456789'+'e-100')      #calculating division 10**100...      
toc = perf_counter() # End Time
T1 = toc - tic
print(f"a finished sec. {T1:1.6f}")
###
tic = perf_counter() # Start Time
b = ('-1.123456789') >> Num('100.0') #calculating division 10**100... 
toc = perf_counter() # End Time
T2 = toc - tic
print(f"b finished sec. {T2:1.6f}")
R = Num.f_perf_time(str(T1), str(T2))                                         # a finished sec. 0.000034  b finished sec. 0.002430 
print('PCT=>', R[0].round(), 'SCALE=>', R[1].round(), 'SQUARENESS=>', a == b) # PCT= -98.6 SCALE= -70.47 SQUARENESS=> True

    ### SCIENTIFIC NOTATION AND HIGH PRECISION RESULTS >>>
from num7 import Num, Num as calc
a = Num('1_000_000_000_000_000_000_000.0') #standard notation
b = Num('1e21') #scientific notation
SUM = a + b #SUM
ieee754 = float(a)+float(b) 
print('SUM == ieee754', SUM == Num(str(ieee754)), ' SUM =>', SUM.num2exp()) #SUM == ieee754 True  SUM => 2e21
###
a = Num('1_000_000_000_000_000_000_000.0') #standard notation
b = Num('1e21') #scientific notation
MUL = a * b #MUL
ieee754 = float(a)*float(b) 
print('MUL == ieee754', MUL == Num(str(ieee754)), ' MUL =>', MUL.num2exp()) #MUL == ieee754 True  MUL => 1e42
###
a = '1.23456789'
b = '9.87654321'
MUL = Num(a) * Num(b) #MUL
ieee754 = float(a)*float(b)
print('MUL == ieee754', MUL == Num(str(ieee754)), 'MUL =>', MUL, float(a)*float(b), '=> IEEE754 PRECISION FAILURE!') #MUL == ieee754 False MUL => 12.1932631112635269 12.193263111263525 => IEEE754 PRECISION FAILURE!
###
a = '1.23456789e320' #scientific notation
b = '9.87654321e320'
MUL = Num(a) * Num(b) #MUL
ieee754 = float(a)*float(b)
print('MUL == ieee754', MUL.str() == str(ieee754), 'MUL =>', MUL.num2exp(), float(a)*float(b), '=> IEEE754 inf FAILURE!') #MUL == ieee754 False MUL => 121932631112635269e624 inf => IEEE754 inf FAILURE!
###
a = '2e320' #scientific notation
b = '3e-320'
MUL = Num(a) * Num(b) #MUL
ieee754 = float(a)*float(b)
print('MUL == ieee754', MUL.str() == str(ieee754), 'MUL =>', MUL.num2exp(), ieee754, '=> IEEE754 inf FAILURE!') #MUL == ieee754 False MUL => 6.0 inf => IEEE754 inf FAILURE!
###
a = '1e200' #scientific notation
b = '5e1200'
T1 = Num(a, 1200) #ultra precision (over 80 digits default) floating point division must be specified!
T2 = Num(b)
DIV = T1 / T2 #DIV
ieee754 = float(a)/float(b)
print('DIV == ieee754', DIV.str() == str(ieee754), 'DIV =>', DIV.num2exp(), ieee754, '=> IEEE754 precision FAILURE!') #DIV == ieee754 False DIV => 2e-1001 0.0 => IEEE754 precision FAILURE!

    ### FLOAT TO NUM CONVERSION LIST >>>
from num7 import Num, Num as calc
L = [1011, 0.0, 9.998412, 7.0, 0.123, -2.0123, 10, 6]
LN= Num.float2num_list(L)
print(list(i.n for i in LN)) #['1011.0', '0.0', '9.998412', '7.0', '0.123', '-2.0123', '10.0', '6.0']
print(list(i for i in LN))   #[Num('1011.0'), Num('0.0'), Num('9.998412'), Num('7.0'), Num('0.123'), Num('-2.0123'), Num('10.0'), Num('6.0')]

    ### SAVE NUMERIC LIST TO DISK FILE >>>
Num.f_filewrite(L) #

    ### READ NUMERIC LIST FROM DISK FILE (nums.txt default filename) >>>
L = Num.f_fileread(); print(L) #[Num('1011.0'), Num('0.0'), Num('9.998412'), Num('7.0'), Num('0.123'), Num('-2.0123'), Num('10.0'), Num('6.0')]

#**************************************************************************************************************#
#*********************** FAQ ************************ FAQ *********************** FAQ *************************#
#**************************************************************************************************************#

Q. I usually try to add 0.1 to 0.2 in python3 with this code:
       >>> print(0.1 + 0.2)
   and the result is:
       >>> 0.30000000000000004
   How instead can it gets exactly 0.3?
A. Using Num class >>>
from num7 import Num, Num as calc
print(Num('0.1') + Num('0.2'))  #calc.add('0.1', '0.2') #0.3

Q. I'll get an arror when i usually type: 
       >>>  Num(0.1) #ValueError: Num.__init__ => float, type not valid: 0.1   
   What is wrong?
A. You must use quotes or string conversion with built-in str function:
       >>> from num7 import Num, Num as calc
       >>> Num('0.1')    #Num('0.1')
       >>> Num(str(0.1)) #Num('0.1')
       
Q. How can i convert a regular float to a Decimal?
A. With Num.ieee754() method >>>
from num7 import Num, Num as calc
a=0.1; b=0.2; 
c=a+b #0.30000000000000004 => PRECISION FAILURE!
an = Num.ieee754(a); print(an)     #0.1000000000000000055511151231257827021181583404541015625
bn = Num.ieee754(b); print(bn)     #0.200000000000000011102230246251565404236316680908203125
cn = Num.ieee754(a+b);
print(cn, '=> PRECISION FAILURE!') #0.3000000000000000444089209850062616169452667236328125 => PRECISION FAILURE!
T = calc.add(an, bn)
print(T, '=> OK.')                 #0.3000000000000000166533453693773481063544750213623046875 => OK.

Q. I have two float variables in my code:
        >>> a = 0.1; b = 0.2
    How can i convert them in Num type?
A. With Num.float2num method (or directly with str() bult-in function) >>>
from num7 import Num, Num as calc
a = 0.1; b = 0.2 #
an= Num.float2num(a); bn= Num.float2num(b) #an= Num(str(a)); bn= Num(str(b))   
print(an+bn, 'OK. VS', a+b, 'PRECISION FAILURE!') #0.3 OK. VS 0.30000000000000004 PRECISION FAILURE!

Q. Can i do add or other math operations also with 10_000 digits after floating point?
A. Yes, you can. >>>
from num7 import Num, Num as calc
print((Num('1.123456789e-10_000') + Num('3.987654321e-10_000')).num2exp()) #511111111e-10008
print((Num('1.123456789e-10_000') - Num('3.987654321e-10_000')).num2exp()) #-2864197532e-10009
print((Num('1.123456789e-10_000') * Num('3.987654321e-10_000')).num2exp()) #4479957319112635269e-20018
print((Num('1.123456789e-10_000') / Num('3.987654321e-10_000'))) #0.28173374584742497292307298769992856660154820877213142969420392746224704666420356

Q. With Python 3.11 it gets an error when running this code >>>

from num7 import Num  
print((Num('1.123456789e-10_000') + Num('3.987654321e-10_000')).num2exp()) #511111111e-10008  

ValueError: Exceeds the limit (4300) for integer string conversion: value has 10010 digits; use sys.set_int_max_str_digits() to increase the limit  

How can i fix it?
A. Set the max string digits allowed in this way >>>

from num7 import Num  
import sys  
sys.set_int_max_str_digits(1_000_000) #1_000_000 str digits set 
print((Num('1.123456789e-10_000') + Num('3.987654321e-10_000')).num2exp()) #511111111e-10008  

'''
