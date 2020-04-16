import random
import itertools
import sys
from utils import *
import argparse


def create_argument_parser():
	parser = argparse.ArgumentParser()
	
	parser.add_argument("-n", "--Boolean", type=int, default=0, help="Boolean Masking Order")
	parser.add_argument("-d", "--Nonlinear", type=int, default=0, help="Nonlinear Representaion Order")
	parser.add_argument("-t", "--Testing", type=bool, default=False, help="Test Encryption")
	parser.add_argument("-R", "--Rounds", type=int, default=10, help="Number of AES Rounds")
	parser.add_argument("-r", "--Run", type=int, default=2, help="Number of encryptions")
	parser.add_argument("-f", "--FixedVsRandom", type=bool, default=False, help="Fixed vs Random test trace")
	
	return parser

########################################################################        
################################# Gadgets ##############################         
########################################################################


#########################################################
# Generate a (n,d)-masking for a list of sensitive bits #
#########################################################
def genMasking(v):
	vm=[]
	for i in range(0,len(v)):
		vm.append([])
		maskBool=0
		maskNlin=1
		vm[i].append([])
		
		for j in range(0,d+1):
			temp=random.randint(0, 1)
			vm[i][0].append(temp)
			maskNlin=maskNlin&temp
		
		for j in range(1,n):
			
			temp=random.randint(0, 1)
			vm[i].append(temp)
			#trace.write("%s" % (temp))
			maskBool=maskBool^vm[i][j]
		
		vm[i].append(maskNlin^maskBool^v[i])

	return vm


################################################
# Remove the masking for a list of masked bits #
################################################
def rmMasking(v):
	t=[]
	for i in range(0,len(v)):
		maskBool=0
		maskNlin=1		
		for j in range(0,d+1):
			maskNlin=maskNlin & v[i][0][j]				
		for j in range(1,n+1):
			maskBool=maskBool ^ v[i][j]
			#trace.write("%s" % (temp))			
		t.append(maskNlin^maskBool)
	return t


###################
# XOR[n,d] Gadget #
###################
def XOR(x,y):  
	z=[]
	z.append([])
	
	x = RefreshMask(x)
	y = RefreshMask(y)
	for i in range(0,d+1):
	
		i1 = x[0][i] ^ y[0][i]
		trace.write("%s" % (i1))
		z[0].append(i1) 

	for i in range(1,n+1):
		i1 = x[i] ^ y[i]
		trace.write("%s" % (i1))
		z.append(i1)

	if   d==0:
	
	 	return z	
	
	elif d==1:
		i1 = x[0][1] & y[0][0] 
		i2 = x[0][0] & y[0][1]
		i3 = i1 ^ i2 
           	
		z[n] = z[n] ^i3

		trace.write("%s%s%s%s" % (i1,i2,i3,z[n]))		
		return z
		
	elif d==2:
		i1  = x[0][0] ^ y[0][0]
		i2  = y[0][2] & i1
		i3  = x[0][2] & y[0][0]
 		i4  = i2 ^ i3
		i5  = x[0][1] & i4
		
		i6  = x[0][2] ^ y[0][2]
		i7  = x[0][0] & i6
		i8  = x[0][2] & y[0][0]
 		i9  = i7 ^ i8
		i10 = y[0][1] & i9
	
		i11 = i10 ^ i5

		z[n] = z[n] ^ i11
		
		trace.write("%s%s%s%s%s%s%s%s%s%s%s%s" % (i1,i2,i3,i4,i5,i6,i7,i8,i9,i10,i11,z[n]))
		
		return z
 		
	else     :
		print 'First you need to define the construction for d=',d
		sys.exit()
	
	

	
	

###################
# AND[n,d] Gadget #
###################
def AND(x,y):
	x = RefreshMask(x)
	y = RefreshMask(y)

	z  = []
	r  = []	
        for i in range(0,n+1):	
		r.append([])		
		for j in range(0,n+1):
			r[i].append(0)

	for i in range(1,n+1):
		for j in range(i+1,n+1):
			r[i][j] = random.randint(0, 1) 
			i1 = x[i] & y[j]
			i2 = x[j] & y[i]
			i3 = r[i][j] ^ i1
			r[j][i] = i3 ^ i2
		
			trace.write("%s%s%s%s%s" % (r[i][j],i1,i2,i3,r[j][i]))
	
		
	if d==0:
		for j in range(1,n+1):		
			r[0][j] = random.randint(0, 1)  			
			#r[j][0] = (r[0][j] ^ (x[0][0] & y[j])) ^ (x[j] & y[0][0])

			i1 = x[0][0] & y[j]
			i2 = x[j] & y[0][0]
			i3 = r[0][j] ^ i1
			r[j][0] = i3 ^ i2
			
			trace.write("%s%s%s%s%s" % (r[0][j],i1,i2,i3,r[j][0]))


		
		z.append([])	
		z[0].append(x[0][0] & y[0][0])	
		trace.write("%s" % (z[0][0]))
		for j in range(1,n+1):
			z[0][0]=z[0][0]^r[0][j]
			trace.write("%s%s" % (r[0][j],z[0][0]))
			
	if d==1:
		z.append([])
		i1 = x[0][0] & y[0][1] 
 		i2 = x[0][1] & y[0][0]
		z[0].append(i1)
		z[0].append(i2)
		trace.write("%s%s" % (i1,i2))
		rn = []
		rn.append([])	
		rn.append([])	
		for i in range(0,n):
			rn[0].append(random.randint(0, 1))  
			rn[1].append(random.randint(0, 1))
			z[0][0]  = z[0][0] ^ rn[0][i]
			z[0][1]  = z[0][1] ^ rn[1][i]
			
			trace.write("%s%s" % (z[0][0],z[0][1]))
		u = 0		
		for i in range(0,n):
			u = u ^ rn[0][i]
			trace.write("%s" % (u))				

		for i in range(1,n+1):
			i1 = x[0][0] & y[i] 
			i2 = rn[0][i-1] & y[0][0]
			i3 = i1 ^ i2
			i4 = x[0][1] & i3
		 		
			i5 = y[0][0] & x[i]
			i6 = rn[1][i-1] & x[0][0]
			i7 = i5 ^ i6
			i8 = y[0][1] & i7
			
			i9 = rn[1][i-1] & u
			i10 = i4 ^ i8

						
			
			r[i][0]=i10 ^ i9

			trace.write("%s%s%s%s%s%s%s%s%s%s%s" % (i1,i2,i3,i4,i5,i6,i7,i8,i9,i10,r[i][0]))
	if d==2:
		z.append([])
		i1 = x[0][0] & y[0][1] 
 		i2 = x[0][1] & y[0][2]
		i3 = x[0][2] & y[0][0]
		z[0].append(i1)
		z[0].append(i2)
		z[0].append(i3)
		trace.write("%s%s%s" % (i1,i2,i3))
		rn = []
		rn.append([])	
		rn.append([])	
		rn.append([])
		for i in range(0,n):
			rn[0].append(random.randint(0, 1))  
			rn[1].append(random.randint(0, 1))
			rn[2].append(random.randint(0, 1))
			z[0][0]  = z[0][0] ^ rn[0][i]
			z[0][1]  = z[0][1] ^ rn[1][i]
			z[0][2]  = z[0][2] ^ rn[2][i]

			trace.write("%s%s%s" % (z[0][0],z[0][1],z[0][2]))
		u = 0		
		for i in range(0,n):
			u = u ^ rn[1][i]
			trace.write("%s" % (u))
		v = 0		
		for i in range(0,n):
			v = v ^ rn[2][i]
			trace.write("%s" % (v))

		for i in range(1,n+1):
			r[i][0] = x[0][0] & ( x[0][2] & (x[0][1] & y[i] ^ rn[0][i-1] & y[0][0] ) ^ rn[1][i-1] & v & y[0][1]) ^ y[0][0] & ( y[0][1] & (y[0][2] & x[i] ^ rn[1][i-1] & x[0][2] ) ^ rn[0][i-1] & u & x[0][2]) ^ x[0][0] & y[0][1] & (rn[1][i-1] & x[0][2] & y[0][0] ^ rn[2][i-1] & x[0][1] & y[0][2]) ^ rn[0][i-1] & x[0][1] & y[0][2] & (v ^ x[0][2] & y[0][0] ) ^ x[0][2] & y[0][0] & (rn[0][i-1] & x[0][0] ^ rn[1][i-1] & y[0][1]) ^ (u & v & rn[0][i-1])
	
	
	for i in range(1,n+1):
		z.append(x[i] & y[i])	
		trace.write("%s" % (z[i]))
		for j in range(0,n+1):
			if j!=i:
				z[i]=z[i]^r[i][j]
				trace.write("%s%s" % (z[i],r[i][j]))
	return z

###########################
# Refreshmask[n,d] Gadget #
###########################
def RefreshMask(x):  
	r=[]
	for i in range(0,d+1):
		r.append(random.randint(0, 1))	

	if d==0:
		x[n] = x[n] ^ r[0]
	if d==1:
		r0 = random.randint(0, 1)
		W = r[0] & (x[0][1] ^ r0) ^ r[1] & (x[0][0] ^ r0)
		R = (r[0] ^ r0) & (r[1] ^ r0) ^ r0
 		x[n] = x[n] ^ W ^ R
	if d==2:
		r0 = random.randint(0, 1)
		W  = r[1] & r[2] & (x[0][0] ^ r0 ) ^ r[0] & r[1] & (x[0][2] ^ r0 ) ^ r[0] & r[2] & (x[0][1] ^ r0 ) ^ r[2] & (x[0][0] ^ r0) & (x[0][1] ^ r0)  ^ r[1] & (x[0][0] ^ r0) & (x[0][2] ^ r0)  ^ r[0] & (x[0][1] ^ r0) & (x[0][2] ^ r0) 
		R  = (r[0] ^ r0) & (r[1] ^ r0) & (r[2] ^ r0) ^ r[2] & r0 & (x[0][0] ^ x[0][1]) ^ r[1] & r0 & (x[0][0] ^ x[0][2]) ^ r[0] & r0 & (x[0][1] ^ x[0][2]) ^ r0
		x[n] = x[n] ^ W ^ R
	
	for i in range(0,d+1):
		x[0][i] = x[0][i] ^ r[i]
	
	for i in range(1,n):
		rb = random.randint(0, 1)
		x[i] = x[i] ^ rb
		x[n] = x[n] ^ rb
	
	return x

###################
# Inv[n,d] Gadget #
###################
def INV(a):

	a[n]=a[n]^1
	
	return a


########################################################################        
################################# AES Functions#########################         
########################################################################

####################################
# Generate a (n,d)-masking for PTX #
####################################
def DataTransformation(vec):
	mvec=[]
	
	for i in range(0,len(vec)):
		mvec.append(genMasking(vec[i]))
	return mvec


####################################
# Print the state in Hex or in Int #
####################################
def printStateHex(vec):
	return decLtohexL(binLtodecL(DataInverseTransformation(vec)))
def printStateInt(vec):
	return binLtodecL(DataInverseTransformation(vec))

##################################
# Remove the masking from a list #
##################################
def DataInverseTransformation(mvec):
	vec=[]
	for i in range(0,len(mvec)):
		vec.append(rmMasking(mvec[i]))
	return vec


################################################
# AES round functions with unrolled round keys #
################################################

roundkeys=[[int(x,16) for x in['2b', '7e', '15', '16', '28', 'ae', 'd2', 'a6', 'ab', 'f7', '15', '88', '09', 'cf', '4f', '3c']],
           [int(x,16) for x in['a0', 'fa', 'fe', '17', '88', '54', '2c', 'b1', '23', 'a3', '39', '39', '2a', '6c', '76', '5' ]],
	   [int(x,16) for x in['f2', 'c2', '95', 'f2', '7a', '96', 'b9', '43', '59', '35', '80', '7a', '73', '59', 'f6', '7f']],
	   [int(x,16) for x in['3d', '80', '47', '7d', '47', '16', 'fe', '3e', '1e', '23', '7e', '44', '6d', '7a', '88', '3b']],
	   [int(x,16) for x in['ef', '44', 'a5', '41', 'a8', '52', '5b', '7f', 'b6', '71', '25', '3b', 'db', '0b', 'ad', '0' ]],
	   [int(x,16) for x in['d4', 'd1', 'c6', 'f8', '7c', '83', '9d', '87', 'ca', 'f2', 'b8', 'bc', '11', 'f9', '15', 'bc']],
	   [int(x,16) for x in['6d', '88', 'a3', '7a', '11', '0b', '3e', 'fd', 'db', 'f9', '86', '41', 'ca', '0', '93', 'fd' ]],
	   [int(x,16) for x in['4e', '54', 'f7', '0e', '5f', '5f', 'c9', 'f3', '84', 'a6', '4f', 'b2', '4e', 'a6', 'dc', '4f']],
	   [int(x,16) for x in['ea', 'd2', '73', '21', 'b5', '8d', 'ba', 'd2', '31', '2b', 'f5', '60', '7f', '8d', '29', '2f']],
	   [int(x,16) for x in['ac', '77', '66', 'f3', '19', 'fa', 'dc', '21', '28', 'd1', '29', '41', '57', '5c', '0', '6e' ]],
	   [int(x,16) for x in['d0', '14', 'f9', 'a8', 'c9', 'ee', '25', '89', 'e1', '3f', '0c', 'c8', 'b6', '63', '0c', 'a6']]]	

def AddRoundKey(ptx,key):
	for i in range(0,len(ptx)):
		ptx[i]=addKey(ptx[i],key[i])
	return ptx


def SubBytes(ptx):
	for i in range(len(ptx)):
		ptx[i]=encSbox(ptx[i])
	return ptx


def ShiftRow(ptx):
	order=[0,5,10,15,4,9,14,3,8,13,2,7,12,1,6,11]
	ptx= [ptx[i] for i in order]
    
  	return ptx

def MixColumn(ptx):
	#print ptx
	mxcInd = [[1, 8, 9, 16, 24], [2, 9, 10, 17, 25], [3, 10, 11, 18, 26], [0, 4, 8, 11, 12, 19, 27], 
	          [0, 5, 8, 12, 13, 20, 28], [6, 13, 14, 21, 29], [0, 7, 8, 14, 15, 22, 30], [0, 8, 15, 23, 31], 
		  [0, 9, 16, 17, 24], [1, 10, 17, 18, 25], [2, 11, 18, 19, 26], [3, 8, 12, 16, 19, 20, 27], 
		  [4, 8, 13, 16, 20, 21, 28], [5, 14, 21, 22, 29], [6, 8, 15, 16, 22, 23, 30], [7, 8, 16, 23, 31], 
		  [0, 8, 17, 24, 25], [1, 9, 18, 25, 26], [2, 10, 19, 26, 27], [3, 11, 16, 20, 24, 27, 28], 
		  [4, 12, 16, 21, 24, 28, 29], [5, 13, 22, 29, 30], [6, 14, 16, 23, 24, 30, 31], [7, 15, 16, 24, 31], 
	          [0, 1, 8, 16, 25], [1, 2, 9, 17, 26], [2, 3, 10, 18, 27], [0, 3, 4, 11, 19, 24, 28], 
		  [0, 4, 5, 12, 20, 24, 29], [5, 6, 13, 21, 30], [0, 6, 7, 14, 22, 24, 31], [0, 7, 15, 23, 24]]
	mtx=[]
	for i in range (0,16):
		mtx.append([])
		for j in range(0,8):
			mtx[i].append([0])

	for col in range(0,4):
		for j in range(0,len(mxcInd)):
			tbyte=j/8+col*4	
			#print (7-mxcInd[j][0]%8)+col*4 ,mxcInd[j][0]/8 ,col
			temp= ptx[mxcInd[j][0]/8+col*4][7-mxcInd[j][0]%8]
			
			for k in range(1,len(mxcInd[j])):
				bitind=7-mxcInd[j][k]%8
				byteind=mxcInd[j][k]/8
				temp=XOR(ptx[byteind+col*4][bitind], temp)
		 
			mtx[j/8+col*4][7-j%8]=temp
				
	#print mtx
	return mtx



def addKey(U,K):
	S=[0]*8
	for i in range(0,8):
		S[i]=XOR(U[i],K[i])	
	return S


def encSbox(U):
	S=[0]*8
	T1=XOR(U[7],U[4])
	T2=XOR(U[7],U[2])
	T3=XOR(U[7],U[1])
	T4=XOR(U[4],U[2])
	T5=XOR(U[3],U[1])
	T6=XOR(T1,T5)
	T7=XOR(U[6],U[5])
	T8=XOR(U[0],T6)
	T9=XOR(U[0],T7)
	T10=XOR(T6,T7)
	T11=XOR(U[6],U[2])
	T12=XOR(U[5],U[2])
	T13=XOR(T3,T4)
	T14=XOR(T6,T11)
	T15=XOR(T5,T11)
	T16=XOR(T5,T12)
	T17=XOR(T9,T16)
	T18=XOR(U[4],U[0])
	T19=XOR(T7,T18)
	T20=XOR(T1,T19)
	T21=XOR(U[1],U[0])
	T22=XOR(T7,T21)
	T23=XOR(T2,T22)
	T24=XOR(T2,T10)
	T25=XOR(T20,T17)
	T26=XOR(T3,T16)
	T27=XOR(T1,T12)
	M1=AND(T13,T6)
	M2=AND(T23,T8)
	M3=XOR(T14,M1)
	M4=AND(T19,U[0])
	M5=XOR(M4,M1)
	M6=AND(T3,T16)
	M7=AND(T22,T9)
	M8=XOR(T26,M6)
	M9=AND(T20,T17)
	M10=XOR(M9,M6)
	M11=AND(T1,T15)
	M12=AND(T4,T27)
	M13=XOR(M12,M11)
	M14=AND(T2,T10)
	M15=XOR(M14,M11)
	M16=XOR(M3,M2)
	M17=XOR(M5,T24)
	M18=XOR(M8,M7)
	M19=XOR(M10,M15)
	M20=XOR(M16,M13)
	M21=XOR(M17,M15)
	M22=XOR(M18,M13)
	M23=XOR(M19,T25)
	M24=XOR(M22,M23)
	M25=AND(M22,M20)
	M26=XOR(M21,M25)
	M27=XOR(M20,M21)
	M28=XOR(M23,M25)
	M29=AND(M28,M27)
	M30=AND(M26,M24)
	M31=AND(M20,M23)
	M32=AND(M27,M31)
	M33=XOR(M27,M25)
	M34=AND(M21,M22)
	M35=AND(M24,M34)
	M36=XOR(M24,M25)
	M37=XOR(M21,M29)
	M38=XOR(M32,M33)
	M39=XOR(M23,M30)
	M40=XOR(M35,M36)
	M41=XOR(M38,M40)
	M42=XOR(M37,M39)
	M43=XOR(M37,M38)
	M44=XOR(M39,M40)
	M45=XOR(M42,M41)
	M46=AND(M44,T6)
	M47=AND(M40,T8)
	M48=AND(M39,U[0])
	M49=AND(M43,T16)
	M50=AND(M38,T9)
	M51=AND(M37,T17)
	M52=AND(M42,T15)
	M53=AND(M45,T27)
	M54=AND(M41,T10)
	M55=AND(M44,T13)
	M56=AND(M40,T23)
	M57=AND(M39,T19)
	M58=AND(M43,T3)
	M59=AND(M38,T22)
	M60=AND(M37,T20)
	M61=AND(M42,T1)
	M62=AND(M45,T4)
	M63=AND(M41,T2)
	L0=XOR(M61,M62)
	L1=XOR(M50,M56)
	L2=XOR(M46,M48)
	L3=XOR(M47,M55)
	L4=XOR(M54,M58)
	L5=XOR(M49,M61)
	L6=XOR(M62,L5)
	L7=XOR(M46,L3)
	L8=XOR(M51,M59)
	L9=XOR(M52,M53)
	L10=XOR(M53,L4)
	L11=XOR(M60,L2)
	L12=XOR(M48,M51)
	L13=XOR(M50,L0)
	L14=XOR(M52,M61)
	L15=XOR(M55,L1)
	L16=XOR(M56,L0)
	L17=XOR(M57,L1)
	L18=XOR(M58,L8)
	L19=XOR(M63,L4)
	L20=XOR(L0,L1)
	L21=XOR(L1,L7)
	L22=XOR(L3,L12)
	L23=XOR(L18,L2)
	L24=XOR(L15,L9)
	L25=XOR(L6,L10)
	L26=XOR(L7,L9)
	L27=XOR(L8,L10)
	L28=XOR(L11,L14)
	L29=XOR(L11,L17)
	S[7]=XOR(L6,L24)
	S[6]=INV(XOR(L16,L26))
	S[5]=INV(XOR(L19,L28))
	S[4]=XOR(L6,L21)
	S[3]=XOR(L20,L22)
	S[2]=XOR(L25,L29)
	S[1]=INV(XOR(L13,L27))
	S[0]=INV(XOR(L6,L23))

	return S
		

def AES_ENC(plaintext,rKeys,R):
	
	binPtx=DataTransformation(decLtobinL(plaintext))
	state=AddRoundKey(binPtx,rKeys[0])
	for i in range(1,R):
		state=SubBytes(state)	
		state=ShiftRow(state)	
		state=MixColumn(state)	
		state=AddRoundKey(state,rKeys[i])

	state=SubBytes(state)	
	state=ShiftRow(state)		
	state=AddRoundKey(state,rKeys[i+1])

	#print 'ciphertext',printState(state)

	return state

########################################################################        
################################# Main #################################         
########################################################################

parser    = create_argument_parser()
arguments = parser.parse_args()
n         = arguments.Boolean 
d         = arguments.Nonlinear 
test      = arguments.Testing 
run       = arguments.Run
rounds    = arguments.Rounds
FnR       = arguments.FixedVsRandom

trace = open('trace.txt','w')

print 'A Naive AES-128 Implementation with Boolean masing order n=',n , ' and NonLinear degree d=',d  

rKeys=[]
for i in range(0, 11):
	rKeys.append(DataTransformation(decLtobinL(roundkeys[i])))


if(test):
	print "---------------- Testing ----------------------------"

	key = ['0x2b','0x7e','0x15','0x16','0x28','0xae','0xd2','0xa6','0xab','0xf7','0x15','0x88','0x09','0xcf','0x4f','0x3c']
	ptx = ['0x32','0x43','0xf6','0xa8','0x88','0x5a','0x30','0x8d','0x31','0x31','0x98','0xa2','0xe0','0x37','0x07','0x34']
	ctx = ['0x39','0x25','0x84','0x1d','0x02','0xdc','0x09','0xfb','0xdc','0x11','0x85','0x97','0x19','0x6a','0x0b','0x32']

	
	
	p = [int(i,0) for i in ptx]	

	print 'Test Key    :',key 
	print 'Test Ptx    :',ptx 
	print 'Test Ctx    :', ctx
	print 'Produced Ctx:', printStateHex(AES_ENC(p,rKeys,rounds))
	trace.write('\n')


	print "---------------- Testing ----------------------------"


print "---------------- Encryption ----------------------------"



for t in range(0,run):
	if(FnR):
		r=random.randrange(2)
		if (r==0):
			ptx = fixedBytes()# Get fixed 16 byte
		else:
			ptx = randomBytes() # Get random 16 byte
		ctx = AES_ENC(ptx,rKeys,rounds)		
		ctx = printStateInt(ctx)
		trace.write('\n')
	else:	
		ptx = randomBytes() # Get random 16 byte
		ctx = AES_ENC(ptx,rKeys,rounds)		
		ctx = printStateInt(ctx)
		trace.write('\n')
	print str(t).zfill(5), ''.join(["{:02X}".format(ptx[i]) for i in range(0,16)]) ,'->', ''.join(["{:02X}".format(ctx[i]) for i in range(0,16)])

trace.close()
plaintext.close()















