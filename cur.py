import numpy as np
import math
import random
def columnselect(A,c,k):
    U,S,V = np.linalg.svd(A,full_matrices = False)
    #print U*S*V
    dimension = A.shape
    a = V.shape
    p = []
    #print a
    for i in xrange(a[0]):
        p.append(sum(V[i,:k]**2))
    #print p
    
    C = np.zeros((dimension[0],c))
    list1 = [i for i in xrange(dimension[1])]
    #print list1
    for t in xrange(c):
        j = random.choice(list1)
        C[:,t] = A[:,j]/(((c**2) * p[j])**0.5)
    return C
A = np.array([[1,2,23],[2,3,4],[3,4,5]])
c = 3
r = 3
k = 3


#U,S,V = np.linalg.svd(A,full_matrices = False)



C = columnselect(A,c,k)
B = A.transpose()
#print A,B
#R = columnselect(B,r,k)
U = np.linalg.pinv(C) * A * np.linalg.pinv(R)
#print C*U*R
