# SUPREME PRECISION GENERAL PURPOSE ARITHMETIC-LOGIC CLASS
    def doc():
        return '''        --- SUPREME PRECISION GENERAL PURPOSE ARITHMETIC-LOGIC CLASS DOCUMENTATION ---

        Num is a lightweight floating point numeric class for arbitrary precision results with always supreme precision.        
        
        Easy to use like school math and WITHOUT IEEE754 ISSUES or +0 AND -0 FAILURES, it can be deployed for
        web e-commerce developing, accounting apps and general math programs included financial ones.
        
        HOW TO USE (integer numeric strings (ex. '2.0') MUST BE SUFFIXED WITH .0):                        
        --- CALCULATOR MODE ---           
                           >>> from num import Num, Num as calc
                           
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
        ROUND:             >>> calc.sqrt('2.0').round(2)  # Num('1.41')
        ABSOLUTE VALUE     >>> calc.abs('-3.0')           # Num('3.0')
        SUM:               >>> cart = ['19.32','18.37','15.13']; calc.sum(*cart)          # Num('52.82')
        MEAN:              >>> cart = ['19.32','18.37','15.13']; calc.mean(*cart).round() # Num('17.61')
        MIN:               >>> cart = ['19.32','18.37','15.13']; calc.min(cart)           # Num('15.13')
        MAX:               >>> cart = ['19.32','18.37','15.13']; calc.max(cart)           # Num('19.32')
        EXP:               >>> calc.mul('-5.3e1024', '2.1e1024').num2exp()                # '-1113E2046'
        REPL:              >>> a = calc('0.1'); b = calc('0.2'); print(calc.add(a, b))    # 0.3

        CODING:
            >>> from num import Num, Num as calc
        
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
                
        ######################## advanced logic programming snippet ########################
    #### LOOP EXAMPLE >>>        
from num import Num, Num as calc
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

    #### ROUNDING AND ACCOUNTING >>>
from num import Num, Num as calc
p = Num('11.19')               #PRICE -Toslink cable for soundbar
pd = round(p.f_price_over(-7)) #PRICE DISCOUNTED 7%
d = round(p - pd)              #DISCOUNT
p_noTAX = round(p.f_price_spinoff(22)) #COST ITEM WITHOUT TAX 22%
TAX = round(p - p_noTAX)               #TAX 22%
print(F'price={p} PAYED={pd} discount={d} COST={p_noTAX} TAX={TAX}') #price=11.19 PAYED=10.41 discount=0.78 COST=9.17 TAX=2.02

    #### PERFORMANCE EVALUATION AND SQUARENESS >>>
####from sys import set_int_max_str_digits #PYTHON 3.11
from num import Num, Num as calc
from time import perf_counter
#set_int_max_str_digits(1_000_000) #PYTHON 3.11
digits = 109
tic = perf_counter() # Start Time
a = Num('-1.123456789'+'e-100')      #calculating division 10**100...      
toc = perf_counter() # End Time
T1 = toc - tic
print(f"a finished sec. {T1:1.6f}")
####
tic = perf_counter() # Start Time
b = ('-1.123456789') >> Num('100.0') #calculating division 10**100... 
toc = perf_counter() # End Time
T2 = toc - tic
print(f"b finished sec. {T2:1.6f}")
R = Num.f_perf_time(str(T1), str(T2))                                         # a finished sec. 0.000034  b finished sec. 0.002430 
print('PCT=>', R[0].round(), 'SCALE=>', R[1].round(), 'SQUARENESS=>', a == b) # PCT= -98.6 SCALE= -70.47 SQUARENESS=> True

    #### SCIENTIFIC NOTATION AND HIGH PRECISION RESULTS >>>
from num import Num, Num as calc
a = Num('1_000_000_000_000_000_000_000.0') #standard notation
b = Num('1e21') #scientific notation
SUM = a + b #SUM
ieee754 = float(a)+float(b) 
print('SUM == ieee754', SUM == Num(str(ieee754)), ' SUM =>', SUM.num2exp()) #SUM == ieee754 True  SUM => 2e21
####
a = Num('1_000_000_000_000_000_000_000.0') #standard notation
b = Num('1e21') #scientific notation
MUL = a * b #MUL
ieee754 = float(a)*float(b) 
print('MUL == ieee754', MUL == Num(str(ieee754)), ' MUL =>', MUL.num2exp()) #MUL == ieee754 True  MUL => 1e42
####
a = '1.23456789'
b = '9.87654321'
MUL = Num(a) * Num(b) #MUL
ieee754 = float(a)*float(b)
print('MUL == ieee754', MUL == Num(str(ieee754)), 'MUL =>', MUL, float(a)*float(b), '=> IEEE754 PRECISION FAILURE!') #MUL == ieee754 False MUL => 12.1932631112635269 12.193263111263525 => IEEE754 PRECISION FAILURE!
####
a = '1.23456789e320' #scientific notation
b = '9.87654321e320'
MUL = Num(a) * Num(b) #MUL
ieee754 = float(a)*float(b)
print('MUL == ieee754', MUL.str() == str(ieee754), 'MUL =>', MUL.num2exp(), float(a)*float(b), '=> IEEE754 inf FAILURE!') #MUL == ieee754 False MUL => 121932631112635269e624 inf => IEEE754 inf FAILURE!
####
a = '2e320' #scientific notation
b = '3e-320'
MUL = Num(a) * Num(b) #MUL
ieee754 = float(a)*float(b)
print('MUL == ieee754', MUL.str() == str(ieee754), 'MUL =>', MUL.num2exp(), ieee754, '=> IEEE754 inf FAILURE!') #MUL == ieee754 False MUL => 6.0 inf => IEEE754 inf FAILURE!
####
a = '1e200' #scientific notation
b = '5e1200'
T1 = Num(a, 1200) #ultra precision (over 80 digits default) floating point division must be specified!
T2 = Num(b)
DIV = T1 / T2 #DIV
ieee754 = float(a)/float(b)
print('DIV == ieee754', DIV.str() == str(ieee754), 'DIV =>', DIV.num2exp(), ieee754, '=> IEEE754 precision FAILURE!') #DIV == ieee754 False DIV => 2e-1001 0.0 => IEEE754 precision FAILURE!

    #### FLOAT TO NUM CONVERSION LIST >>>
from num import Num, Num as calc
L = [1011, 0.0, 9.998412, 7.0, 0.123, -2.0123, 10, 6]
LN= Num.float2num_list(L)
print(list(i.n for i in LN)) #['1011.0', '0.0', '9.998412', '7.0', '0.123', '-2.0123', '10.0', '6.0']
print(list(i for i in LN))   #[Num('1011.0'), Num('0.0'), Num('9.998412'), Num('7.0'), Num('0.123'), Num('-2.0123'), Num('10.0'), Num('6.0')]

    #### SAVE NUMERIC LIST TO DISK FILE >>>
Num.f_filewrite(L) #

    #### READ NUMERIC LIST FROM DISK FILE (nums.txt default filename) >>>
L = Num.f_fileread(); print(L) #[Num('1011.0'), Num('0.0'), Num('9.998412'), Num('7.0'), Num('0.123'), Num('-2.0123'), Num('10.0'), Num('6.0')]

####**************************************************************************************************************#
####*********************** FAQ ************************ FAQ *********************** FAQ *************************#
####**************************************************************************************************************#

Q. I usually try to add 0.1 to 0.2 in python3 with this code:
       >>> print(0.1 + 0.2)
   and the result is:
       >>> 0.30000000000000004
   How instead can it get exactly 0.3?
A. Using Num class >>>
from num import Num, Num as calc
print(Num('0.1') + Num('0.2'))  #calc.add('0.1', '0.2') #0.3

Q. I'll get an arror when i usually type: 
       >>>  Num(0.1) #ValueError: Num.__init__ => float, type not valid: 0.1   
   What is wrong?
A. You must use quotes or string conversion with built-in str function:
       >>> from num import Num, Num as calc
       >>> Num('0.1')    #Num('0.1')
       >>> Num(str(0.1)) #Num('0.1')
       
Q. How can i convert a regular float to a Decimal?
A. With Num.ieee754() method >>>
from num import Num, Num as calc
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
from num import Num, Num as calc
a = 0.1; b = 0.2 #
an= Num.float2num(a); bn= Num.float2num(b) #an= Num(str(a)); bn= Num(str(b))   
print(an+bn, 'OK. VS', a+b, 'PRECISION FAILURE!') #0.3 OK. VS 0.30000000000000004 PRECISION FAILURE!

Q. Can i do add or other math operations also with 10_000 digits after floating point?
A. Yes, you can. >>>
from num import Num, Num as calc
print((Num('1.123456789e-10_000') + Num('3.987654321e-10_000')).num2exp()) #511111111e-10008
print((Num('1.123456789e-10_000') - Num('3.987654321e-10_000')).num2exp()) #-2864197532e-10009
print((Num('1.123456789e-10_000') * Num('3.987654321e-10_000')).num2exp()) #4479957319112635269e-20018
print((Num('1.123456789e-10_000') / Num('3.987654321e-10_000'))) #0.28173374584742497292307298769992856660154820877213142969420392746224704666420356

'''