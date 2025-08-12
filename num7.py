''' --- SUPREME PRECISION GENERAL PURPOSE ARITHMETIC-LOGIC DECIMAL CLASS --- (SEE DOC AT THE END) ''' 

class Num:
    ''' object self attributes list allowed ''' 
    __slots__ = ('d', 'n', 'n0', 'n1', 'n2', 'L_n0', 'L_n1')
    
    ''' class VARIABLES list ''' 
    pi = '3.141592654'
    e  = '2.718281828'
    
    ''' class METHODS list  ''' 
    
    def f_fund_fr(self, i, y) -> 'Num':
        ''' french financing month mortgage (high precision) '''
        i = Num(i) / 100 
        return (self*i) / (1-(1+i)**-y) / 12 #
    
    def f_fund_IEEE754(S, i, y) -> float:
        ''' french financing month mortgage (high speed) '''
        i = i / 100 
        return (S*i) / (1-(1+i)**-y) / 12
    
    def f_perf(self, sob) -> 'Num':
        ''' percentage performance value (direct ratio) '''
        sob = Num(sob) #allowing float string as: '2.3'
        return (-self + sob) / self * 100
    
    def f_perf_time(self, sob) -> tuple:
        ''' percentage and relative magnitude order time performance value (inverse ratio) '''
        sob = Num(sob) #allowing float string as: '2.3'
        self= Num(self)
        R = ((self - sob) / sob * 100)
        return R, -sob/self+1 if sob>self else self/sob-1 # tuple
    
    def f_price_over(self, t = 22) -> 'Num':
        ''' add or sub a percentage value to a base price ''' 
        t = Num(t) #allowing float string as: '2.3'
        self += self * t / 100
        return self
    
    def f_price_spinoff(self, t = 22) -> 'Num':
        ''' spin off percentage tax value from a base price ''' 
        t = Num(t) #allowing float string as: '2.3'
        return self / ((100+t) / 100)
    
    def f_fileread(filename = 'nums.txt') -> list:
        ''' read a number strings column from disk ''' 
        FILE = [ls for line in open(filename, 'r') if (ls:=line.strip())]
        cart = [Num(str(N)) if '.' in N else Num(str(N)+'.0') for N in FILE]
        return cart 
    
    def f_filewrite(L: list, filename = 'nums.txt') -> None:
        ''' write a number strings column on disk ''' 
        lines = [f'{str(i)}\n' for i in L]
        with open(filename, 'a') as FILE:
            FILE.writelines(lines)
        return None

    def str(self) -> str:
        ''' return Num string '''
        return self.__str__()

    def repr(self) -> str:
        ''' return Num representation string '''
        return self.__repr__()
    
    def is_numstr(n) -> bool:
        ''' is_numstr to check numeric string validation '''
        if type(n) != str:
            return False      
        if 'E' in n.upper():            
            n = Num.exp2num(n)
        nv = n.split('.')
        if len(nv) != 2 or not (type(int(nv[0])) == int and nv[1].isdigit()): 
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

    def is_numint(self) -> bool:
        ''' is_numint checks if integer num '''
        if self.n1 == '0':
            return True
        return False

    def is_numfloat(self) -> bool:
        ''' is_numfloat checks if floating point num '''
        if self.n1 != '0':
            return True
        return False

    def is_numeven(self) -> bool:
        ''' is_numeven checks if even num '''
        if self.is_numint():
            if self % 2:
                return False
            return True
        raise ValueError("Num.is_numeven => Num, must be integer value: ", self)
    
    def is_numodd(self) -> bool:
        ''' is_numodd checks if odd num '''
        if self.is_numint():
            if self % 2:
                return True
            return False
        raise ValueError("Num.is_numodd => Num, must be integer value:", self)																			  
    
    def exp2num(s) -> str:
        ''' convert a scientific notation number to string numeric '''
        if type(s) != str:
            raise ValueError("Num.exp2num => type not valid:", s)																 
        s = s.strip().upper()
        be = s.split('E'); be0 = be[0]; be1 = be[1]
        if len(be) > 2:
            raise ValueError("Num.exp2num => scientific notation not valid:", s)    																					
        try:
            float(be0); float(be1)
        except:
            raise ValueError("Num.exp2num => scientific notation not valid:", s)																		
        if be1 == '-0' or be1 == '+0':
            raise ValueError("Num.exp2num => zero can not be signed:", s)    																			 
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

    def ieee754(self) -> str: 
        ''' float to IEEE754 conversion '''
        return f'{float(self):.80f}'.rstrip('0')

    def float2num(f) -> 'Num':
        ''' float to Num conversion '''
        return Num(str(f)) 

    def float2num_list(L: list) -> list:
        ''' float to Num list conversion '''
        return [Num((i) if type(i)==int else str(i)) for i in L]
    
    def num2exp(ob) -> str:
        ''' convert a Num object to scientific notation string '''
        if type(ob) != Num:
            raise ValueError("Num.num2exp => type not valid:", ob)  
        if ob.n1 == '0': #EXP >= 0
            e = ob.L_n0 - 1
            CHECK = (ob.n0[0] + '.' + ob.n0[1:]).rstrip('0')
            if CHECK[-1] == '.':
                CHECK += '0'
            return ob.n2 + CHECK + 'e' + str(e)
        if ob.n0 == '0': #EXP < 0
            n1 = ob.n1.lstrip('0')
            L_n1 = len(n1)
            e = ob.L_n1 - L_n1 + 1
            if L_n1 == 1:
                return ob.n2 + n1 + '.0' + 'e' + str(-e)
            return ob.n2 + n1[-L_n1:-L_n1+1] + '.' + n1[-L_n1+1:] + 'e' + str(-e)
        e = ob.L_n0 - 1
        return ob.n2 + ob.n0[0] + '.' + ob.n0[1:] + ob.n1 + 'e' + str(e)
    
    def numint(self) -> 'Num':
        ''' Num integer truncation '''
        return Num(self.n2 + self.n0 + '.0')
    
    def trunc(self, d = 0) -> 'Num':
        ''' Num floating point truncation '''
        m = Num(10)**d
        return Num(int(self * m), d) / m

    def round_floor(self, d = 0) -> 'Num': #relative value (real number R)
        ''' Num floor rounding '''
        ''' relative round down: 0.12 => 0.1 -0.12 => -0.2 '''
        if self >= 0: #positives and zero 
            return self.trunc(d)
        #negatives
        e = Num('1.0', d) / Num('10.0')**d
        if d >= 0:
            t = self.trunc(d) - e; t2 = self - e
            return self if t == t2 else t            
        if e < self:
            return self
        t = self.trunc(d) - e; t2 = self - e
        return self if t == t2 else t            
    
    def round(self, d = 2) -> 'Num':
        ''' Num half up rounding '''
        ''' COMMON STANDARD -relative round_half_ceil: 0.15 => 0.2 -0.15 => -0.1 '''
        temp = (self + Num('0.5') * Num('10.0')**-d).round_floor(d)
        return temp
        
    def round_bank(self, d = 2) -> 'Num':
        ''' Num half even rounding '''
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
                    return Num(self.n2 + str(a) + '.0') #12.6 => 13.0 integer
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
                    if not int(self.n0) and int(self.n1) == 5:	# self.n0 == 0 and self.n1 == 5 (ex. -0.00000005 => 0.0)
                        return Num('0.0') # ZERO SYMMETRIC MEETING
                    return Num(self.n2 + self.n0 + '.' + self.n1[0:d-1] + str(a)) #even 5.65 => 5.6 -0.05 => 0.0
            else: 
                try:
                    return Num(self.n2 + self.n0 + '.' + self.n1[0:d-1] + str(a)) #3.1415 => 3.14 #-0.02 => -0.0 ERROR!
                except:
                    return Num('0.0') #-0.02 => 0.0 OK.
    
    def round_ceil(self, d = 0) -> 'Num':
        ''' Num ceil rounding '''
        ''' relative round up: 0.12 => 0.2 -0.12 => -0.1 '''
        if self <= 0: #negatives and zero 
            return self.trunc(d)
        #positives
        e = Num('1.0', d) / Num('10.0') ** d
        if d <= 0:
            t = self.trunc(d) + e; t2 = self + e
            return self if t == t2 else t            
        if e > self:
            return self
        t = self.trunc(d) + e; t2 = self + e
        return self if t == t2 else t            
                    
    def reduce(itb, init=None, f=lambda x, y: x+y):
        ''' used by sum() '''
        i = iter(itb)
        x = next(i) if init is None else init
        for y in i:
            x = f(Num(x), Num(y))
        return x

    def sum(*multi_args: tuple) -> 'Num': 
        ''' calculator sum method '''
        return Num.reduce(multi_args)

    def mean(*multi_args: tuple) -> 'Num': 
        ''' calculator mean method '''
        return Num.reduce(multi_args)/len(multi_args)
    
    def min(L: list) -> 'Num': 
        ''' calculator min method '''
        return min([Num(i) for i in L])
    
    def max(L: list) -> 'Num': 
        ''' calculator max method '''
        return max([Num(i) for i in L])

    def root_i(n, i = 3, d = 80) -> 'Num':
        ''' calculator ith root method '''
        if not i:
            return('1.0')
        n = Num(n, d); i = Num(i)
        if i.is_numeven() and n.n2:
            raise ValueError("Num.root_i => Negative number:", n)																 
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
                raise ValueError("Num.root_i => d parameter too low:", d)																		 
            z = t//i
        s = str(s)   
        if d: #floating point conversion with clearing zeros        
            s = '0' * (1 + d - len(s)) + s
            r = (s[:-d] + '.' +s[-d:]).rstrip('0') 
            s = r + '0' if r[-1] == '.' else r
            return Num(sign + s)
        return Num(sign + s + '.0') #integer conversion

    def sqrt(n, d = 80) -> 'Num':
        ''' calculator square root method '''
        n = Num(n)
        if n.L_n0 > 80 and d == 80:
            return Num.sqr(n, n.L_n0)
        return Num.sqr(n, d)
    
    def sqr(n, d = 80) -> 'int Num':
        ''' square root method => used by sqrt() '''
        ''' sqr(n, d = 80) method runs on python3 trying to be more human style
            and so overcoming sqrt() integer arithmetic limits. (math library function)
        '''                                       
        d = abs(int(d))

        if type(n) == int: #only integer square root (not floating point)        
            if n < 0:
                raise ValueError("Num.sqr => Negative number:", n)																  
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
                raise ValueError("Num.sqr => Negative number:", n)															  
                   
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
            raise ValueError("Num.sqr => 'float', type not valid:", n)																	  
        else:
            raise ValueError("Num.sqr => Type not valid:", n)															 

    def _divi_(n, div, d=3) -> str:
        ''' division between signed integer number '''
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

    def __hash__(self) -> int:
        if int(self.n1): #floating point
            return hash(self.n)
        else: 			 #integer
            return int(self.n2 + self.n0)

    def __init__(self, n, d = 80) -> 'Num':
        ''' Num object constructor '''  
        #VALIDATION n
        if type(n) == int:
            n = str(n) + '.0' # SUFFIX .0 FOR 'int' type        
        if type(n) == float:
            raise ValueError("Num.__init__ => float, type not valid:", n)            																					 
        if type(n) == Num:
            self.d    = n.d if d < n.d else d
            self.n    = n.n
            self.n0   = n.n0
            self.n1   = n.n1
            self.n2   = n.n2 
            self.L_n0 = n.L_n0
            self.L_n1 = n.L_n1         
            return None
        if type(n) != str:
            raise ValueError("Num.__init__ => type not valid:", n)    																	  
        if 'E' in n.upper():            
            n = Num.exp2num(n)        
        nv = n.split('.')
        if len(nv) != 2 or not (type(int(nv[0])) == int and nv[1].isdigit()): #.isnumeric() .isdigit() .isdecimal()
            raise ValueError("Num.__init__ => number format not valid:", n)                   																							  
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
            self.n1 = self.n1.rstrip('0') #clear RIGHT zeros
            if not len(self.n1): #if ''
                self.n1 = '0'                
        self.L_n0 = len(self.n0); self.L_n1 = len(self.n1) #check for new len       
        self.n = self.n2 + self.n0 + '.' + self.n1         #set all number cleaned 
        if self.n0 == '0' and self.n1 == '0': # zero get not any sign == BE CAREFUL!
            if self.n2 == '-' or n[0] == '+':
                raise ValueError("Num.__init__ => zero can not be signed:", n)    																				  
        self.d = d if d > (self.L_n0 + self.L_n1) else (self.L_n0 + self.L_n1) #precision

    def __bool__(self) -> bool:
        ''' not logic unary operator '''
        return False if self.n == '0.0' else True

    def __invert__(self) -> 'Num':
        ''' (~) not unary bitwise operator '''
        if not Num.is_numint(self) or self.n2: #only positive integer
            raise TypeError("Num.__invert__ => only positive integer allowed:", self)        																							 
        t = ''
        for bit in bin(int(self.n0))[2:]:
            t += '0' if bit == '1' else '1'
        return Num(int(t, 2))
    
    def __and__(self, sob) -> int:
        ''' (&) overloading binary & operator (Bitwise AND) '''
        if not Num.is_numint(self) or self.n2: #only positive integer
            raise TypeError("Num.__and__ => only positive integer allowed:", self)        																						  
        if type(sob) == int or Num.is_numstr(sob):
            sob = Num(sob)
        if not Num.is_numint(sob) and sob >= 0: #only integer
            raise TypeError("Num.__and__ => only positive integer allowed:", sob)              																							   
        if type(sob) != Num:
            raise TypeError("Num.__and__ => type not valid:", sob)        																		  
        return int(self.n0) & int(sob.n0)

    def __rand__(self, sob) -> int: 
        ''' (&) swap operands binary AND bitwise operator '''
        return Num(sob).__and__(self)

    def __or__(self, sob) -> int:
        ''' (|) overloading binary | operator (Bitwise OR) '''
        if not Num.is_numint(self) or self.n2: #only positive integer
            raise TypeError("Num.__or__ => only positive integer allowed:", self)       																						
        if type(sob) == int or Num.is_numstr(sob):
            sob = Num(sob)
        if not Num.is_numint(sob):   #only integer
            raise TypeError("Num.__or__ => only positive integer allowed:", self)            																							 
        if type(sob) != Num:
            raise TypeError("Num.__or__ => type not valid:", sob)        																		 
        return int(self.n0) | int(sob.n0)

    def __ror__(self, sob) -> int: 
        ''' (|) swap operands binary OR bitwise operator '''
        return Num(sob).__or__(self)

    def __xor__(self, sob) -> int:
        ''' (^) overloading binary ^ operator (Bitwise XOR) '''
        if not Num.is_numint(self) or self.n2: #only positive integer
            raise TypeError("Num.__xor__ => only positive integer allowed:", self)        																						  
        if type(sob) == int or Num.is_numstr(sob):
            sob = Num(sob)
        if not Num.is_numint(sob):   #only integer
            raise TypeError("Num.__xor__ => only positive integer allowed:", self)             																							   
        if type(sob) != Num:
            raise TypeError("Num.__xor__ => type not valid:", sob)        																		  
        return int(self.n0) ^ int(sob.n0)

    def __rxor__(self, sob) -> int:
        ''' (^) swap operands binary XOR bitwise operator '''
        return Num(sob).__xor__(self)
    
    def __abs__(self) -> 'Num':        
        ''' (built-in abs function) Return the absolute value of a number '''
        return Num(self.n if self.n2 == '' else self.n[1:]) 
    
    def abs(self) -> 'Num':
        ''' abs method calculator '''
        return Num(self).__abs__()

    def add(a, b) -> 'Num':
        ''' (+) calculator addition method '''
        return Num(a) + Num(b)
        
    def __add__(self, sob) -> 'Num':
        ''' (+) overloading binary plus operator -used by built-in method sum() '''
        if type(sob) == int or Num.is_numstr(sob):
            sob = Num(sob)
        if type(sob) != Num:
            raise TypeError("Num.__add__( => type not valid:", sob)																   
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
        return Num(xt[0:-xt_D] + '.' + xt[-xt_D:])
    
    def inc(self, sob = 1) -> 'Num':
        ''' increment variable adding method -object modify by self reference '''
        telf = self + sob
        self.d    = telf.d
        self.n    = telf.n
        self.n0   = telf.n0
        self.n1   = telf.n1
        self.n2   = telf.n2 
        self.L_n0 = telf.L_n0
        self.L_n1 = telf.L_n1         
        return self
    
    def incmul(self, sob = 10) -> 'Num':
        ''' increment variable multiplying method -object modify by self reference '''
        telf = self * sob
        self.d    = telf.d
        self.n    = telf.n
        self.n0   = telf.n0
        self.n1   = telf.n1
        self.n2   = telf.n2 
        self.L_n0 = telf.L_n0
        self.L_n1 = telf.L_n1         
        return self
    
    def dec(self, sob = 1) -> 'Num':
        ''' decrement variable subtracting method -object modify by self reference '''
        telf = self - sob
        self.d    = telf.d
        self.n    = telf.n
        self.n0   = telf.n0
        self.n1   = telf.n1
        self.n2   = telf.n2 
        self.L_n0 = telf.L_n0
        self.L_n1 = telf.L_n1         
        return self
    
    def decdiv(self, sob = 10) -> 'Num':
        ''' decrement variable dividing method -object modify by self reference '''
        telf = self / sob
        self.d    = telf.d
        self.n    = telf.n
        self.n0   = telf.n0
        self.n1   = telf.n1
        self.n2   = telf.n2 
        self.L_n0 = telf.L_n0
        self.L_n1 = telf.L_n1         
        return self
    
    def clear(self) -> 'Num':
        ''' clear variable '''
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
    
    def sub(a, b) -> 'Num':
        ''' (-) calculator subtract method '''
        return Num(a) - Num(b)

    def __sub__(self, sob) -> 'Num': 
        ''' (-) overloading binary minus operator '''
        if type(sob) == int or Num.is_numstr(sob):
            sob = Num(sob)
        if type(sob) != Num:
            raise TypeError("Num.__add__( => type not valid:", sob)																  
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
        return Num(xt[0:-xt_D] + '.' + xt[-xt_D:])
    
    def __rsub__(self, sob) -> 'Num': 
        ''' (-) swap operands binary minus operator '''
        return Num(sob).__sub__(self)
            
    def mul(a, b) -> 'Num':
        ''' (*) calculator multiplication method '''
        return Num(a) * Num(b)
    
    def __mul__(self, sob) -> 'Num': 
        ''' (*) overloading binary multiply operator '''
        if type(sob) == int or Num.is_numstr(sob):
            sob = Num(sob)
        if type(sob) != Num:
            raise TypeError("Num.__mul__ => type not valid:", sob)																  
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
    
    def __lshift__(self, sob) -> 'Num':
        ''' (<<) left shift binary operator -multiplying for 10 powers '''
        return self * 10**int(Num(sob)) #
    
    def __rlshift__(self, sob) -> 'Num':
        ''' (<<) swap operands left shift binary operator '''
        return Num(sob).__lshift__(self)
        
    ''' (*) swap operands binary multiplication operator '''
    __rmul__ = __mul__ 
    
    def div(a, b) -> 'Num':
        ''' (/) calculator division method '''
        return Num(a) / Num(b)
    
    def __truediv__(self, sob) -> 'Num': 
        ''' (/) overloading binary floating point division operator  '''
        if type(sob) == int or Num.is_numstr(sob):
           sob = Num(sob)
        if type(sob) != Num:
            raise TypeError("Num.__truediv__ => type not valid:", sob)																	  
        if sob == '0.0':
            raise Exception('Num.__truediv__ => ZeroDivisionError: Num division by zero')
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

    def __rtruediv__(self, sob) -> 'Num':
        ''' (/) swap operands floating point division binary operator  '''
        return Num(sob).__truediv__(self)
    
    def __floordiv__(self, sob) -> 'Num': 
        ''' (//) overloading integer division binary operator '''
        if type(sob) == int or Num.is_numstr(sob):
            sob = Num(sob)
        if type(sob) != Num:
            raise TypeError("Num.__floordiv__ => type not valid:", sob)																	   
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
    
    def __rfloordiv__(self, sob) -> 'Num': 
        ''' (//) swap operands integer division binary operator '''
        return Num(sob).__floordiv__(self)

    def __mod__(self, sob) -> 'Num': 
        ''' (%) overloading module binary operator (Num floating point division remainder) '''
        if type(sob) == int or Num.is_numstr(sob):
            sob = Num(sob)
        if type(sob) != Num:
            raise TypeError("Num.__floordiv__ => type not valid:", sob)																  
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

    def __rmod__(self, sob) -> 'Num':
        ''' (%) swap operands module operator (integer division remainder) '''
        return Num(sob).__mod__(self)

    def divmod(self, sob) -> tuple:    
        ''' (// %) calculator divmod return a tuple (self // sob, self % sob) '''
        Q = Num(self).__floordiv__(Num(sob))
        R = Num(self).__mod__(Num(sob))
        return Q, R

    def __divmod__(self, sob) -> tuple:    
        ''' (divmod built-in method) return a tuple (self // sob, self % sob) '''
        Q = (self).__floordiv__((sob))
        R = (self).__mod__((sob))
        return Q, R

    def __rdivmod__(self, sob) -> 'Num': 
        ''' (divmod built-in method) swap operands '''
        return Num(sob).__divmod__(self)
    
    def __rshift__(self, sob) -> 'Num':
        ''' (>>) right shift binary operator -dividing for ten powers '''
        sob = Num(sob)
        t = sob + self.L_n1
        self.d = t if t > self.d else self.d
        return self / 10**int(sob) 
    
    def __rrshift__(self, sob) -> 'Num':
        ''' (>>) swap operands right shift binary operator '''
        return Num(sob).__rshift__(self)
                   
    def __eq__(self, sob) -> bool: #== !=
        ''' (== !=) overloading equal and not equal logic binary operators '''
        sob = Num(sob)
        return True if self.n == sob.n else False
    
    def __gt__(self, sob) -> bool: #>
        ''' (>) overloading greater logic binary operator '''
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

    def __ge__(self, sob) -> bool: #>=
        ''' (>=) overloading greater or equal logic binary operator '''
        return True if self > sob or self == sob else False

    def __lt__(self, sob) -> bool: #<
        ''' (<) overloading less logic binary operator '''
        return False if self >= sob else True #

    def __le__(self, sob) -> bool: #<=
        ''' (<=) overloading less or equal logic binary operator '''
        return False if self > sob else True  #
    
    def __len__(self) -> int:
        ''' overloading built-in method len() '''
        return len(self.n)
    
    def len(self) -> tuple:
        ''' return a tuple with num lengths before and after floating point dot '''
        return len(self.n0), 0 if len(self.n1) == 1 and self.n1 == '0' else len(self.n1)       
    
    def __neg__(self) -> 'Num':
        ''' overloading unary operator - '''
        return Num(self.n[1:]) if self.n2 == '-' else Num('-' + self.n)
    
    def __pos__(self) -> 'Num':
        ''' overloading unary operator + '''
        return Num(self.n)
    
    def __int__(self) -> int: 
        ''' (built-in int method) Num to int (truncation) - great loss precision! '''
        return int(self.n2 + self.n0) 

    def int(self) -> int: 
        ''' (truncation) Num to int method - great loss precision! '''
        return self.__int__()

    def __float__(self) -> float: 
        ''' Num to float (loss precision!) '''
        return float(self.n)

    def pow(self, e) -> 'Num':
        ''' pow method calculator '''
        return Num(self).__pow__(Num(e))        
    
    def __pow__(self, e) -> 'Num': #argument e mandatory,  
        ''' (**) overloading power binary operator and used by built-in function pow() '''
        if type(e) != int and type(e) != Num:
            raise ValueError("Num.__pow__ => type not valid:", e)            																			 
        if type(e) == int or type(e) == Num and e.is_numint():            
            if self == Num('0.0') and e == 0:
                raise ValueError("Num.__pow__ => undetermined:", e) 
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
        raise ValueError("Num.__pow__ => Num, must be integer value:", e)																		 
    
    def __rpow__(self, sob) -> 'Num': 
        ''' (**) swap operands power binary operator '''
        return Num(sob).__pow__(self)

    def __round__(self, d = 2) -> 'Num':   
        ''' built-in function round() '''
        return self.round(d)
    
    def __trunc__(self) -> int: 
        ''' like math.trunc() function '''
        return self.__int__()
    
    def __str__(self) -> str:   
        ''' built-in function str() '''
        return self.n

    def __repr__(self) -> str: #almost like __str__ (obj representation in REPL)
        ''' built-in function repr() '''
        return str('Num(\'' + self.n + '\')')

    def __format__(self, spec) -> str:
        if self.is_numint():
            return int(self.n2 + self.n0).__format__(spec)
        else:
            return float(self.n).__format__(spec)

    def doc() -> str: 
        return '''        --- SUPREME PRECISION GENERAL PURPOSE ARITHMETIC-LOGIC DECIMAL CLASS DOCUMENTATION ---

        Num is a lightweight floating point numeric class for arbitrary precision results with always supreme precision.        
        
        Easy to use like school math and WITHOUT IEEE754 ISSUES or +0 AND -0 FAILURES, it can be deployed for
        web e-commerce developing, accounting apps and general math programs included financial ones.
		Compatible with MicroPython also a Rasperry pi pico can work with almost num7 capability. 
        
        HOW TO USE (integer numeric strings (ex. '2.0') MUST BE SUFFIXED WITH .0):                        
        --- CALCULATOR MODE ---           
                           >>> from num7 import Num, Num as calc
                           
        ADDITION:          >>> calc.add('-5.3', '2.1')    #Num('-3.2')
        SUBTRACTION:       >>> calc.sub('-5.3', '2.1')    #Num('-7.4')
        MULTIPLICATION:    >>> calc.mul('-5.3', '2.1')    #Num('-11.13')
        DIVISION:          >>> calc.div('-5.3', '2.1')    #Num('-2.52380952380952380952380952380952380952380952380952380952380952380952380952380952')
        M+:                >>> M = calc('0.0'); M.inc('3.0'); M.inc('3.3'); M.inc('3.7'); print(M) #10.0
        M-:                >>>                  M.dec('5.0'); M.dec('3.3'); M.dec('1.5'); print(M) #0.2
        MC:                >>> M.clear(); print(M) # 0.0
        INT   DIV AND REM: >>> calc.divmod('5.0', '3.0')  #(Num('1.0'), Num('2.0')) => tuple 
        FLOAT DIV AND REM: >>> calc.divmod('5.2', '3.1')  #(Num('1.0'), Num('2.1')) => tuple
        POWER:             >>> calc.pow('-5.3', '2.0')    #Num('28.09')
        SQRT:              >>> calc.sqrt('2.0')           #Num('1.41421356237309504880168872420969807856967187537694807317667973799073247846210703')
        ROOT_ith           >>> calc.root_i('1.860867', 3) #Num('1.23')
        ROUND:             >>> calc.sqrt('2.0').round(2)  #Num('1.41')
        ABSOLUTE VALUE     >>> calc.abs('-3.0')           #Num('3.0')
        SUM:               >>> cart = ['19.32','18.37','15.13']; calc.sum(*cart)          #Num('52.82')
        MEAN:              >>> cart = ['19.32','18.37','15.13']; calc.mean(*cart).round() #Num('17.61')
        MIN:               >>> cart = ['19.32','18.37','15.13']; calc.min(cart)           #Num('15.13')
        MAX:               >>> cart = ['19.32','18.37','15.13']; calc.max(cart)           #Num('19.32')
        EXP:               >>> calc.mul('-5.3e1024', '2.1e1024').num2exp()                #'-1.113e2049'
        REPL:              >>> a = calc('0.1'); b = calc('0.2'); print(calc.add(a, b))    #0.3

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

            #bitwise operators
from num7 import Num
print('--- (&) AND ---')
op1 = Num('3.0')
op2 = 5
print(f'{int(op1):08b}', op1) #00000011 3.0
op1 &= op2                    #AND
print(f'{op2:08b}', op2)      #00000101 5
print(f'{int(op1):08b}', op1) #00000001 1

print('--- (|) OR  ---')
op1 = Num('3.0')
op2 = 5
print(f'{int(op1):08b}', op1) #00000011 3.0
op1 |= op2                    #OR
print(f'{op2:08b}', op2)      #00000101 5
print(f'{int(op1):08b}', op1) #00000111 7

print('--- (^) XOR ---')
op1 = Num('3.0')
op2 = 5
print(f'{int(op1):08b}', op1) #00000011 3.0
op1 ^= op2                    #XOR
print(f'{op2:08b}', op2)      #00000101 5
print(f'{int(op1):08b}', op1) #00000110 6

print('--- (<<) LEFT SHIFT -X10 MULTIPLIER ---')
op1 = Num('1.0')
op2 = 2
print(f'{int(op1):08b}', op1) #00000001 1.0
op1 <<= op2                   #LEFT SHIFT -X10 MULTIPLIER
print(f'{op2:08b}', op2)      #00000010 2
print(f'{int(op1):08b}', op1) #01100100 100.0

print('--- (>>) RIGHT SHIFT -X10 DIVIDER ---')
op1 = Num('250.0')
op2 = 1
print(f'{int(op1):08b}', op1) #11111010 250.0
op1 >>= op2                   #RIGHT SHIFT -X10 DIVIDER
print(f'{op2:08b}', op2)      #00000001 1
print(f'{int(op1):08b}', op1) #00011001 25.0

print('--- (~) NOT ---')
op1 = Num('10.0')
print(f'{int(op1):08b}', op1) #00001010 10.0
op2 = ~op1                    #(~) NOT
print(f'{int(op2):08b}', op2) #00000101 5.0

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
print(a, 'INTEGER =>', a.is_numint(), 'EVEN =>', a.is_numeven()) #6.0 INTEGER => True EVEN => True 
print(b, 'INTEGER =>', b.is_numint(), 'ODD  =>', b.is_numodd())  #3.0 INTEGER => True ODD  => True  
print(c, 'FLOAT  =>', c.is_numfloat())                           #3.14 FLOAT  => True

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
R = Num.f_perf_time(str(T1), str(T2))                                         # a finished sec. 0.000029  b finished sec. 0.000125 
print('PCT=>', R[0].round(), 'SCALE=>', R[1].round(), 'SQUARENESS=>', a == b) # PCT=> -76.74 SCALE=> -3.3 SQUARENESS=> True
#stock exchange assets performance  
previous = Num('26.96'); now = Num('27.27')  
var_pct = Num.f_perf(previous, now).round()  
print(f'{float(var_pct):+.2f}') #'26.96' -> '27.27' => +1.15

    ### SCIENTIFIC NOTATION AND HIGH PRECISION RESULTS >>>
from num7 import Num, Num as calc
a = Num('1_000_000_000_000_000_000_000.0') #standard notation
b = Num('1e21') #scientific notation
SUM = a + b #SUM
ieee754 = float(a)+float(b) 
print('SUM == ieee754', SUM == Num(str(ieee754)), ' SUM =>', SUM.num2exp()) #SUM == ieee754 True  SUM => 2.0e21
###
a = Num('1_000_000_000_000_000_000_000.0') #standard notation
b = Num('1e21') #scientific notation
MUL = a * b #MUL
ieee754 = float(a)*float(b) 
print('MUL == ieee754', MUL == Num(str(ieee754)), ' MUL =>', MUL.num2exp()) #MUL == ieee754 True  MUL => 1.0e42
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
print('MUL == ieee754', MUL.str() == str(ieee754), 'MUL =>', MUL.num2exp(), float(a)*float(b), '=> IEEE754 inf FAILURE!') #MUL == ieee754 False MUL => 1.21932631112635269e641 inf => IEEE754 inf FAILURE!
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
print('DIV == ieee754', DIV.str() == str(ieee754), 'DIV =>', DIV.num2exp(), ieee754, '=> IEEE754 precision FAILURE!') #DIV == ieee754 False DIV => 2.0e-1001 0.0 => IEEE754 precision FAILURE!

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
print((Num('1.123456789e-10_000') + Num('3.987654321e-10_000')).num2exp()) #5.11111111e-10000
print((Num('1.123456789e-10_000') - Num('3.987654321e-10_000')).num2exp()) #-2.864197532e-10000
print((Num('1.123456789e-10_000') * Num('3.987654321e-10_000')).num2exp()) #4.479957319112635269e-20000  
print((Num('1.123456789e-10_000') / Num('3.987654321e-10_000'))) #0.28173374584742497292307298769992856660154820877213142969420392746224704666420356

Q. With Python 3.11 it gets an error when running this code >>>

from num7 import Num  
print((Num('1.123456789e-10_000') + Num('3.987654321e-10_000')).num2exp()) #5.11111111e-10000  

ValueError: Exceeds the limit (4300) for integer string conversion: value has 10010 digits; use sys.set_int_max_str_digits() to increase the limit  

How can i fix it?
A. Set the max string digits allowed in this way >>>

from num7 import Num  
import sys  
sys.set_int_max_str_digits(1_000_000) #1_000_000 str digits set 
print((Num('1.123456789e-10_000') + Num('3.987654321e-10_000')).num2exp()) #5.11111111e-10000  

Q. I must enter many integer variables in my code:  

	>>> a = Num('123.0'); b = Num('456.0'); c = Num('789.0')
	
Can i input them without quotes and suffix .0?  
A. Yes, this way:

	>>> a = Num(123); b = Num(456); c = Num(789)  

'''
