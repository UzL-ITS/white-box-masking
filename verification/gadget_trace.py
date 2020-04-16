#!/usr/bin/env python2
#-*- coding:utf-8 -*-
import argparse
import math
from itertools import product

from tree import OptBitNode as Bit
from tree.trace import circuit_trace
from tree.anf import compute_anfs
OP = Bit.OP

def create_argument_parser():
	parser = argparse.ArgumentParser()
	
	parser.add_argument("-n", "--Boolean", type=int, default=0, help="Boolean Masking Order")
	parser.add_argument("-d", "--Nonlinear", type=int, default=0, help="Nonlinear Representaion Order")
	parser.add_argument("-t", "--Target", type=str, default='', help="Target Gadget")	
	return parser

parser    = create_argument_parser()
arguments = parser.parse_args()
n         = arguments.Boolean 
d         = arguments.Nonlinear 
t         = arguments.Target 


if n==1 and d==1:
	from schemes import Minimalist3
	S = Minimalist3()
	x = Bit.inputs("x", S.N)
	y = Bit.inputs("y", S.N)
	rx = Bit.inputs("rx", S.NR)
	ry = Bit.inputs("ry", S.NR)
	if t=='XOR':
		target = S.EvalXOR(x, y, rx, ry)
	elif t=='AND':
		target = S.EvalAND(x, y, rx, ry)
	elif t=='RefreshMask':
		target = S.Refresh(*(x + rx)) + S.Refresh(*(y+ry))

	else: 
		target = S.EvalXOR(x, y, rx, ry) + S.EvalAND(x, y, rx, ry)


if n==2 and d==1:
	from schemes import Hybrid21
	S = Hybrid21()
	x = Bit.inputs("x", S.N)
	y = Bit.inputs("y", S.N)
	rx = Bit.inputs("rx", S.NR)
	ry = Bit.inputs("ry", S.NR)
	rz = Bit.inputs("rz", S.randomNode)

	if t=='XOR':
		target = S.EvalXOR(x, y, rx, ry)
	elif t=='AND':
		target = S.EvalAND(x, y, rx, ry,rz)
	elif t=='RefreshMask':
		target = S.Refresh(*(x + rx)) + S.Refresh(*(y+ry))
	else: 
		target = S.EvalXOR(x, y, rx, ry) + S.EvalAND(x, y, rx, ry,rz)

if n==3 and d==1: 
	from schemes import Hybrid31
	S = Hybrid31()
	x = Bit.inputs("x", S.N)
	y = Bit.inputs("y", S.N)
	rx = Bit.inputs("rx", S.NR)
	ry = Bit.inputs("ry", S.NR)
	rz = Bit.inputs("rz", S.randomNode)

	if t=='XOR':
		target = S.EvalXOR(x, y, rx, ry)
	elif t=='AND':
		target = S.EvalAND(x, y, rx, ry,rz)
	elif t=='RefreshMask':
		target = S.Refresh(*(x + rx)) + S.Refresh(*(y+ry))
	else: 
		target = S.EvalXOR(x, y, rx, ry) + S.EvalAND(x, y, rx, ry,rz)


print S
print


if 1: # compute ANFs and bias bound
    for bit in target:
        compute_anfs(bit)
    nodes = Bit.flatten_many(target)

    maxdeg = 0
    res = []
    for b in sorted(nodes, key=lambda b: b.id):
        if b.op in (b.OP.AND, b.OP.OR):
            print b.id, "=", b.OP.name[b.op], " ".join(map(str, [sub.id for sub in b.args if isinstance(sub, Bit)])), ":",
            print "degree on r %d, full %d:" % (b.meta["anf"].degree(filter_func=lambda v: v.startswith("r")), b.meta["anf"].degree()),
            print b.meta["anf"]
            res.append(b.meta["anf"])
        elif b.is_input():
            print b.id, "=", b.name(), ":", b.meta["anf"]
            res.append(b.meta["anf"])
        else:
            assert b.op in (b.OP.XOR, b.OP.NOT, b.OP.INPUT)

    print

    maxdeg = max(a.degree(filter_func=lambda v: v.startswith("r")) for a in res)
    from fractions import Fraction
    print "------------------------------------------"
    print "Maximum degree:", maxdeg
    bias = abs(Fraction(1, 2)-Fraction(1, 2**maxdeg))
    print "Bias bound: bias <= %s" % bias
    e = -math.log(0.5 + bias, 2)
    print "Provable security:"
    try:
        print " 80 bit: R > %d" % (80 * (1 + 1/e))
        print "128 bit: R > %d" % (128 * (1 + 1/e))
    except:
        pass
    print "------------------------------------------"
    print

def sbin(x, n):
    return "".join(map(str, tobin(x, n)))

def tobin(x, n):
    return tuple(map(int, bin(x).lstrip("0b").rjust(n, "0")))

if 1: # trace the circuit to perform linear algebra analysis in Sage
    #input_order = x + y + rx + ry + rz
    if n <= 1 or t=='XOR':
    	input_order = x + y + rx + ry
    else :
   	input_order = x + y + rx + ry + rz

    inputs = list(product(range(2), repeat=len(input_order))) 
     
#    for i in range(len(inputs)):
#	print inputs[i]
    
    print len(input_order) 
    trace = circuit_trace(outputs=target, input_order=input_order, inputs_list=inputs)
   
    ntraces = len(inputs)
   
    order = sorted(trace.keys(), key=lambda bit: bit.id)

    order = [b for b in order if b.op != b.OP.XOR and not b.is_const()]
   
    with open("traces/%s" % S.NAME, "w") as f:
        with open("traces/%s.names" % S.NAME, "w") as fi:
            cntr = 0
            for bit in order:
                if bit.is_input():
                    name = bit.name()
	           
                else:
                    name ="v%d" % cntr
                    cntr += 1
		
                value = trace[bit]
		#print type(sbin(value, ntraces))
                f.write("%s`%s\n" % (name, sbin(value, ntraces)))

                info = bit.meta.get("tag", "") + ":"# + str(bit)
                info = info.strip(":")
                fi.write("%s`%s\n" % (name, info))

    print "Traces written" ,cntr
