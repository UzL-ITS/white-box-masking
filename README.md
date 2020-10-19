This repository contains the scripts that used in the paper "A White-Box Masking Scheme Resisting Computational and Algebraic Attacks" and it contains two main directories:
- AES-128:
	-- AESmain.py: A python script for (n,0), (n,1) and (n,2) masked schemes. 
	-- analysis.m: A matlab script for the analysis. 
- Verification:
	-- The scripts to run the algebraic verification of the gadgets in the paper.


# AES-128 Implementation

AES-128 Implementation contains (n,0), (n,1) and (n,2) masked schemes. The python implementation produces two .txt files, 'plaintext.txt' and 'trace.txt' that can be used to implement DCA or Fixed vs Random leakage test. 

- '-n' : Boolean Masking Order (an arbitrary value) 
- '-d' : Nonlinear Representaion Order (0, 1 or 2 to generate an implementation d>2 one has to first generate the construction)
- '-t' : Test Encryption (to test the correctness of the construction)
- '-R' : Number of AES rounds
- '-r' : Number of encryptions
- '-f' : Leakage test mode using fixed vs random plaintext. (default: False) In order to run a Fixed vs Random test this mode should be used!


`python AESmain.py -n 3 -d 1 -r 5 -t True`

A Naive AES-128 Implementation with Boolean masing order n= 3  and NonLinear degree d= 1 
```
---------------- Testing ---------------------------- 
Test Key    : ['0x2b', '0x7e', '0x15', '0x16', '0x28', '0xae', '0xd2', '0xa6', '0xab', '0xf7', '0x15', '0x88', '0x09', '0xcf', '0x4f', '0x3c'] 
Test Ptx    : ['0x32', '0x43', '0xf6', '0xa8', '0x88', '0x5a', '0x30', '0x8d', '0x31', '0x31', '0x98', '0xa2', '0xe0', '0x37', '0x07', '0x34']
Test Ctx    : ['0x39', '0x25', '0x84', '0x1d', '0x02', '0xdc', '0x09', '0xfb', '0xdc', '0x11', '0x85', '0x97', '0x19', '0x6a', '0x0b', '0x32'] 
Produced Ctx: ['0x39', '0x25', '0x84', '0x1d', '0x02', '0xdc', '0x09', '0xfb', '0xdc', '0x11', '0x85', '0x97', '0x19', '0x6a', '0x0b', '0x32'] 
---------------- Testing ----------------------------
---------------- Encryption ----------------------------
00000 7C3B2E9DA7BA06ADCBE015994268FA49 -> 55568EBB32CA9AF497CCFF0C7A218161
00001 286BB9975D9510F4EFEC78D6DA767ECA -> 4163F0EE51D45DFA852A980C372A89C7
00002 F84D1A38FAE424E7EEFA7BB27FAEA3D1 -> F93A3957EBC0BE6834032E8AC2C1FEC1
00003 302330A0AC0534C7E4A7C2960F13DF35 -> 4195D14E5D3BBEB0236A521773CFCFDB
00004 93CCB3D6C70863DF27E6CE22B2708BD8 -> 84547C4FAE95DE1DEF0C35F9D1D55C89
```

`python AESmain.py -n 4 -d 1 -r 10`

```
A Naive AES-128 Implementation with Boolean masing order n= 4  and NonLinear degree d= 1
---------------- Encryption ----------------------------
00000 4A9535FCDF0DCAFE345A17E98B00FFB8 -> E7DFA37D90938170477B457149227A1A
00001 B8C1CE0756DE2EECCB841FD4F5F76CA2 -> 4001F6D7E26804C4B1AD767726335AE7
00002 FA4B2C4C809989256BCFB7AAAF202FE5 -> 4939DA4A517357D7C6D30EE8841DB8E4
00003 4BEB1FDBAB88E4F06A53D14ABAD5FFFC -> 0B528E578673F03C589261CD612BC12B
00004 376C5760D661A09A58AEA72206C0FC76 -> A6A26DE3B5F868E5AD4B992F77DE3718
00005 E07D3F063511F8DBECFBE197DA59619D -> 6124DCB427453D9C31DECDC1D6EC7ADD
00006 790232CD2525D9F4F848A6D382AF44FB -> B9F291088D20D8B20371A6AD078615B9
00007 E2C7E9B757C14AD6E8FC16A67DC1DF80 -> D481BD2D2BC34B078A632BFFFD68660D
00008 5426B0C5392E54781A0C81648EAF0F0D -> 404F53BFD7DDE52544FF04323ED8E8CA
00009 323C4A755B6B3742006241E80C627D7D -> 64CB311C2E7F5913F92448C73C349334
```

`python AESmain.py -n 2 -d 1 -r 10  -f True` 
```
A Naive AES-128 Implementation with Boolean masing order n= 2  and NonLinear degree d= 1
Fixed vs Random mode Selected: 10 encryption will be processed using fixed or random plaintexts
---------------- Encryption ----------------------------
00000 BF4E303BA9BEADB4F885F3A130257D43 -> 9E3E58F4E9142F9F1921A1871404A140
00001 00000000000000000000000000000000 -> 7DF76B0C1AB899B33E42F047B91B546F
00002 B9437574B1C1E2528C59BBED105F0629 -> 99E92E2EAFD331B17BBB44DC690C610D
00003 C276573DE9EB5C71CF802B48EC212ECF -> 4FE393795779FB94F15D33455A68FD93
00004 0A9EEBBBD1F418D6633F05456DADA3F6 -> E5C9B0FE169EB644F9392E35753525DE
00005 00000000000000000000000000000000 -> 7DF76B0C1AB899B33E42F047B91B546F
00006 00000000000000000000000000000000 -> 7DF76B0C1AB899B33E42F047B91B546F
00007 FC6BC0327BDDC58D54FD573F82CDE4E8 -> 91260635B09C65668E38E475B55F6E75
00008 9442060573A13E5E3E85DA0188770CBB -> A3784CD1325572F3026AF785106BB2E6
00009 00000000000000000000000000000000 -> 7DF76B0C1AB899B33E42F047B91B546F
```

# Differential Computation Analysis

analyis.m contains the matlab code for the analysis. It inputs two file 'plaintext.txt' and 'trace.txt' and proceed a basic DCA attack using these files. The file contains DCA attacks and t-test (using the software trace collected by FvR mode of AES-128  implementation). 

# MaskVerif

The verification uses the tool MaskVerif: https://cryptoexperts.com/maskverif/ 
The gadget codes can be directly used with MaskVerif.

`./maskverif < order4_2/and_sni.mv ` 


# Algebraic verification

The experimental verification of first-order algebraic security of gadgets: 
- Xor[1,1], And[1,1], RefreshMask[1,1]
- Xor[2,1], And[2,1], RefreshMask[2,1]
- Xor[3,1], And[3,1], RefreshMask[3,1]


The verification algorithm adapted from https://github.com/cryptolu/whitebox. It works as identical to the original source:

- first, gadget_trace.py script to generate traces.
- Second, gadget_check.py to run the verification algorithm.

Further information can be found in: https://github.com/cryptolu/whitebox

However, in order to verify the correct gadgets  gadget_trace.py should be adapted and the following inputs are needed:


- '-n' : Boolean Masking Order (an arbitrary value) 
- '-d' : Nonlinear Representaion Order (0, 1 or 2 to generate an implementation d>2 one has to first generate the construction)
- '-t' : Target gadget (XOR, AND or RefreshMask)

To check the original masking defined in [BU18]:

- 'python gadget_trace.py -n 1 -d 1 -t XOR'
- 'sage gadget_check.py traces/minimalist'

To check the (2,1)-Gadgets: 

- 'python gadget_trace.py -n 2 -d 1 -t XOR'
- 'sage gadget_check.py traces/hybrid'
