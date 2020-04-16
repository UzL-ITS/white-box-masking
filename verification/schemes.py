#-*- coding:utf-8 -*-
import random
class Scheme(object):
    N = NotImplemented
    NR = NotImplemented
    NAME = NotImplemented

    def __str__(self):
        return "<Scheme %s N=%d NR=%d>" % (self.NAME, self.N, self.NR)

# (1,1)-scheme [BU18] Minimalist Quadratic Masking
class Minimalist3(Scheme):
    N = 3
    NR = 3
    NAME = "minimalist3"

    def Decode(self, x):
        a, b, c = x
        return (a & b) ^ c

    def Refresh(self, x, y, z, rx, ry, rr):
        if 1: # secure
            xrr = x ^ rr
            yrr = y ^ rr
            rz = (rx & yrr) ^ (ry & xrr) ^ ((rx ^ rr) & (ry ^ rr)) ^ rr
        else: # insecure
            rz = (rx & y) ^ (ry & x) ^ (rx & ry)

        x ^= rx
        y ^= ry
        z ^= rz
        return x, y, z

    def EvalXOR(self, x, y, rx, ry):
        x = self.Refresh(*(x + rx))
        y = self.Refresh(*(y + ry))

        a, b, c = x
        d, e, f = y
        ae = a & e
        bd = b & d
        a_d = a ^ d
        b_e = b ^ e
        x = a_d
        y = b_e
        z = c ^ f ^ ae ^ bd
        return x, y, z

    def EvalAND(self, x, y, rx, ry):
        zero = rx[0] ^ rx[0]
        x = self.Refresh(*(x + rx))
        y = self.Refresh(*(y + ry))

        a, b, c = x
        d, e, f = y

        rf = ry[2]
        rc = rx[2]
        # rf = rc = zero # introduces another insecurity

        x = (a & e) ^ rf
        y = (b & d) ^ rc

        triple1 = ((c & e) ^ (b & rf)) & d
        triple2 = ((b & f) ^ (e & rc)) & a
        double = c & f
        fix = rf & rc

        z = triple1 ^ triple2 ^ double ^ fix
        return x, y, z



# (2,1)-scheme Example 2
class Hybrid21(Scheme):
    N = 4
    NR = 4
    randomNode= 5
    NAME = "hybrid"

    def Decode(self, x):
        a, b, c , d = x
        return (a & b) ^ c ^ d

    def Refresh(self, x00, x01, x1, x2, r00, r01, r0,r1):
	#print x,y,z,t,rx, ry, rr,rt
	x00 = x00 ^ r00
	x01 = x01 ^ r01

	x1 = x1  ^ r1
	x2 = x2  ^ r1	
	
	W =  r00 & (x01 ^ r0) ^ r01 & (x00 ^ r0)
 	R = (r00 ^ r0) & (r01 ^ r0) ^ r0


	x2  = x2  ^ W ^ R
	
        return x00, x01, x1 ,x2

    def EvalXOR(self, x, y, rx, ry):
	#print 'bc', x ,rx
        x = self.Refresh(*(x + rx))
	#print 'ac',x         
	y = self.Refresh(*(y + ry))

        x00,x01,x1,x2 = x
        y00,y01,y1,y2 = y

	z00 = x00 ^ y00
	z01 = x01 ^ y01
	z1  = x1  ^ y1
	z2  = x2  ^ y2 
        
	U = x00 & y01 ^ x01 & y00
	
      	z2 = z2 ^ U
        return z00, z01, z1, z2

    def EvalAND(self, x, y, rx, ry,rz):
        zero = rx[0] ^ rx[0]
        x = self.Refresh(*(x + rx))
        y = self.Refresh(*(y + ry))

        x00,x01,x1,x2 = x
        y00,y01,y1,y2 = y
	
	r01, r02, r11, r12, r_12 = rz

	z00  = x00 ^ y01 ^ r01 ^ r02
	z01  = x01 ^ y00 ^ r11 ^ r12	
	
	r10 = x01 & (x00 & y1 ^ r01 & y00) ^ y01 & (y00 & x1 ^ r11 & x00)  ^ r11 & ( r01 ^ r02 )	
	r20 = x01 & (x00 & y2 ^ r02 & y00) ^ y01 & (y00 & x2 ^ r12 & x00)  ^ r12 & ( r01 ^ r02 )

	# r12 = r0 & r1 ^ r0 & r3 ^ r2 & r1 ^ r2 & r3
	
	
	r21 = (x2 & y1) ^ (x1 & y2 ^ r_12)

	z1  = x1 & y1  ^ r10 ^ r_12  
	
	z2  = x2 & y2  ^ r20 ^ r21
	#############################
        
        return z00, z01, z1, z2 



# (3,1)-scheme Example 2
class Hybrid31(Scheme):
    N = 5
    NR = 5
    randomNode= 6
    NAME = "hybrid"

    def Decode(self, x): 
        a, b, c, d, e = x
        return (a & b) ^ c ^ d ^ e

    def Refresh(self, x00, x01, x1, x2, x3, r00, r01, r0, r1 ,r2):
	#print x,y,z,t,rx, ry, rr,rt
	x00 = x00 ^ r00
	x01 = x01 ^ r01

	x1 = x1 ^ r1	
	x3 = x3 ^ r1	

	x2 = x2 ^ r2 
	x3 = x3 ^ r2
	
	W =  r00 & (x01 ^ r0) ^ r01 & (x00 ^ r0)
 	R = (r00 ^ r0) & (r01 ^ r0) ^ r0


	x3  = x3  ^ W ^ R
	
        return x00, x01, x1, x2, x3 

    def EvalXOR(self, x, y, rx, ry): 
	#print 'bc', x ,rx
        x = self.Refresh(*(x + rx))
	#print 'ac',x         
	y = self.Refresh(*(y + ry))

        x00, x01, x1, x2, x3 = x
        y00, y01, y1, y2, y3 = y

	z00 = x00 ^ y00
	z01 = x01 ^ y01
	z1  = x1  ^ y1
	z2  = x2  ^ y2 
	z3  = x3  ^ y3 
        
	U = x00 & y01 ^ x01 & y00
	
      	z3 = z3 ^ U
        return z00, z01, z2, z3, z3

    def EvalAND(self, x, y, rx, ry,rz):
        zero = rx[0] ^ rx[0]
        x = self.Refresh(*(x + rx))
        y = self.Refresh(*(y + ry))

	x00, x01, x1, x2, x3 = x
        y00, y01, y1, y2, y3 = y
	
	r01, r02, r03, r11, r12, r13 = rz


	r_12 = random.randint(0, 1)
	r_13 = random.randint(0, 1)
	r_23 = random.randint(0, 1)
	

	z00  = x00 ^ y01 ^ r01 ^ r02 ^ r03
	z01  = x01 ^ y00 ^ r11 ^ r12 ^ r12	
	
	r10 = x01 & (x00 & y1 ^ r01 & y00) ^ y01 & (y00 & x1 ^ r11 & x00)  ^ r11 & ( r01 ^ r02 )	
	r20 = x01 & (x00 & y2 ^ r02 & y00) ^ y01 & (y00 & x2 ^ r12 & x00)  ^ r12 & ( r01 ^ r02 )
	r30 = x01 & (x00 & y3 ^ r03 & y00) ^ y01 & (y00 & x3 ^ r13 & x00)  ^ r13 & ( r01 ^ r02 )

	# r12 = r0 & r1 ^ r0 & r3 ^ r2 & r1 ^ r2 & r3
	
	
	r21 = (x2 & y1) ^ (x1 & y2 ^ r_12)
	r31 = (x3 & y1) ^ (x1 & y3 ^ r_13)
	r32 = (x2 & y3) ^ (x3 & y2 ^ r_23)

	z1  = x1 & y1  ^ r10 ^ r_12 ^ r_13  
	z2  = x2 & y2  ^ r20 ^ r21  ^ r_23	
        z3  = x3 & y3  ^ r30 ^ r31  ^ r32

	z2  = x2 & y2  ^ r20 ^ r21
	#############################
        
        return z00, z01, z1, z2 ,z3





















