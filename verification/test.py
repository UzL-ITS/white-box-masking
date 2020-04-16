from sage.all import *


x_0 = var('x_0')
x_1 = var('x_1')
x_2 = var('x_2')
y_0 = var('y_0')
y_1 = var('y_1')
y_2 = var('y_2')
r_0 = var('r_0')
r_1 = var('r_1')
r_2 = var('r_2')
r_3 = var('r_3')
r_4 = var('r_4')
r_5 = var('r_5')
a1   = var('a1')
b1   = var('b1')
a2   = var('a2')
b2   = var('b2')



a= (x_0*y_1+r_0+r_1)*(x_1*y_2+r_2+r_3)*(x_2*y_0+r_4+r_5)-(x_2* (x_1 * (x_0 * a1 + (r_0 + r_1) * r_4 * y_2) + r_2 * y_0 * ((r_0 + r_1) + x_0 * y_1))            + r_4 * x_1 * y_2 * ((r_0 + r_1) * x_2 + (r_0 + r_1))+y_2* (y_1 * (y_0 * b1 + (r_2 + r_3) * r_4 * x_0) +       x_1 * ( r_4 * x_0 * y_1 + r_0 * x_2 * y_0)) + r_4 * x_0 * y_1 * ((r_2 + r_3) * y_2 + (r_2 + r_3))+x_2* (x_1 * (x_0 * a2 + (r_0 + r_1) * r_5 * y_2) + r_3 * y_0 * ((r_0 + r_1) + x_0 * y_1))            + r_5 * x_1 * y_2 * ((r_0 + r_1) * x_2 + (r_0 + r_1))+y_2 *(y_1 * (y_0 * b2 + (r_2 + r_3) * r_5 * x_0) +       x_1 * ( r_5 * x_0 * y_1 + r_1 * x_2 * y_0)) + r_5 * x_0 * y_1 * ((r_2 + r_3) * y_2 + (r_2 + r_3)))

print expand(a)
#import itertools

#trace=[]

#for i in range(0,28):
#	trace.append(i)
#	


#print trace


#temp=list(itertools.combinations(trace, 2))

#i=list(temp[0])



#print i[0],i[1]



