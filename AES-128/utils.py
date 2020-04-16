import itertools
import random

##########################
# Binary list to decimal #
# [0,0,1,1,] ==> 3       #
##########################
def bin2dec(a):
	tmp=0
	for i in range(0,len(a)):
		tmp=tmp+2**(m-i-1)*a[i]
	return tmp


###########################################################
# Calculate the hammning weight of a list		  # 
###########################################################	

def HW(a):
	hw=0
	for i in range(0,len(a)):
		hw=hw+a[i]
	return hw

#######################
# Inverse 0-->1, 1-->0 #   
########################
def inv2(a):
	return (a+1)%2


#######################
# Binary list to hex  #
# [0,0,1,1,] ==> 0x03 #
#######################	
def bintohex(a):

	if isinstance(a[0], int):
		t=''
		for j in range(0,len(a)):
			t=t+str(a[len(a)-j-1])	
	
		return hex(int(t, 2))
	else:	
		tt=[]
		for i in range(0,len(a)):
			t=''
			for j in range(0,len(a[i])):
				t=t+str(a[i][len(a[i])-j-1])
			tt.append(hex(int(t, 2)))
		return tt

def shifting(bitlist):
	bitlist=list(reversed(bitlist))
	out = 0
	for bit in bitlist:
		out = (out << 1) | bit
	return out

	
#######################################################
# Generate a (n,d)-masking for PTX #
#######################################################
def DataTransformation(vec):
	mvec=[]
	
	for i in range(0,len(vec)):
		mvec.append(genMasking(vec[i]))
	return mvec

##################################
# Remove the masking from a list #
##################################
def DataInverseTransformation(mvec):
	vec=[]
	for i in range(0,len(mvec)):
		vec.append(rmMasking(mvec[i]))
	return vec


#######################	
# Binary list to hex  #
# [0,0,1,1,] ==> 0x03 #
#######################	
def decLtobinL(vec):
	binvec=[]
	for i in range(0,len(vec)):
		binvec.append([int(x) for x in bin(vec[i])[2:].zfill(8)][::-1])
	return binvec

		
#######################
# Binary list to hex  #
# [0,0,1,1,] ==> 0x03 #
#######################	
def binLtodecL(vec):
	binvec=[]
	for i in range(0,len(vec)):
		binvec.append(shifting(vec[i]))
	return binvec


#######################
# Binary list to hex  #
# [0,0,1,1,] ==> 0x03 #
#######################	
def decLtohexL(vec):
	hexvec=[]
	for i in range(0,len(vec)):
		hexvec.append("0x{:02x}".format(vec[i]))
	return hexvec

		

def printState(vec):
	return decLtohexL(binLtodecL(DataInverseTransformation(vec)))

def randomBytes():
	ptx=[]	
	for ind in range (0, 16):
		ptx.append(random.randrange(256))
		plaintext.write("%s " %ptx[ind])	
	plaintext.write('\n')
        return ptx
def fixedBytes():
	ptx=[]	
	for ind in range (0, 16):
		ptx.append(0)
		plaintext.write("%s " %ptx[ind])	
	plaintext.write('\n')
        return ptx

plaintext = open('plaintext.txt','w')





