import numpy as np
import math
import random
'''
	Attempt at LeverageScore CUR.
	
	Constructs matrices C and R based on "column leverage scores" and "row leverage scores of input matrix A.
'''
def random_pick(list1,prob):
	print "kitteh"
	return 2

def complevscore(A,k,flag):
	'''
		flag = 0 if row leverage
		flag = 1 if column leverage
	'''
	U,S,V = np.linalg.svd(A,full_matrices = False)
	
	if flag == 0:
		score = np.sum(U[:,:k]**2,axis = 1)
	elif flag==1:
		score = np.sum(V[:k,:]**2,axis = 0)
	
	normalize_score = score/k
	
	return score, normalize_score

def columnselect(A,c,r,k,flag):
	'''
		function for selecting which row and which column
		
		flag = 0 row select
		flag = 1 column select
		
	'''
	a = A.shape
	C = np.zeros((a[0],c))
	R = np.zeros((r,a[1]))
	
	if flag == 1:
		
		colLev = complevscore(A,k,flag)
		list1 = [i for i in xrange(a[1])]
		
		for x in xrange(c):
			j = random_pick(list1,min(1,c*colLev[x]))
			C[:,x] = A[:,j]/(math.sqrt(c**2 * colLev[x]))
		return C
	
	
	elif flag == 0:
		rowLev = complevscore(A,k,flag)
		list2 = [i for i in xrange(a[0])]
		for y in xrange(r):
			k = random_pick(list2,min(1,r*rowLev[y]))
			R[y,:] = A[k,:]/(math.sqrt(r**2 * rowLev[y]))
		return R

def CUR(A,c,r,k):
	C = columnselect(A,c,r,k,1)
	R = columnselect(A,c,r,k,0)
	U = np.linalg.pinv(C) * A * np.linalg.pinv(R)
	return C,U,R

if __name__=="main":
	c = 10
	r = 100
	k = 5
	A = [[1,2,3],[2,3,4],[4,5,6]]
	C,U,R = CUR(A,c,r,k)
