"""
	Assignment #2
	Project: To implement both SVD and CUR Matrix decomposition algorithms and 
	compare their efficency (in terms of space, time etc.)

	Instructor: Dr. Aruna Malapati

	Contributors: G V Sandeep 2014A7PS106H
                  Kushagra Agrawal 2014AAPS334H
                  Snehal Wadhwani 2014A7PS430H

	Course: CS F469 Information Retrieval

"""

import numpy as np
import math
from numpy import linalg as LA

input_file = open("test.txt","r")
rating_raw = input_file.readlines()
rating_list = []

for line in rating_raw:
	ind_rating = []
	line = line.split(" ")

	user = int(line[0])
	ind_rating.append(user)

	item = int(line[1])
	ind_rating.append(item)

	rating = float(line[2])
	ind_rating.append(rating)	
	rating_list.append(ind_rating)

max_item = 0
max_user = rating_list[len(rating_list)-1][0]
for rating in rating_list:
	if rating[1] > max_item:
		max_item = rating[1]

ratings = np.zeros((max_user, max_item))

for rating in rating_list:
	ratings[rating[0]-1][rating[1]-1] = rating[2]


"""
'''
Caluclating the Frobenius Error obtained by using the inbuilt SVD package of Python
'''
U,sigma,V = LA.svd(ratings,full_matrices=False)
final_sigma = np.zeros((len(sigma),len(sigma)))
for i in range(0,len(sigma)):
	final_sigma[i][i] = sigma[i]


ratings_svd = np.dot(U, np.dot(final_sigma, V))

error = 0

for i in range(0,len(ratings)):
	for j in range(0,len(ratings[i])):
		error = error + (ratings[i][j]-ratings_svd[i][j])**2

error = math.sqrt(error) # IDEAL FROBENIUS ERROR 

"""


"""
Implemntation of SVD
"""


'''
TRIDIAGONALIZATION
GIVEN A SQUARE MATRIX, CALCULATION OF IT's HOUSEHOLDER TRIDIAGONAL TRANSFORMATION
Input : ratings X ratings.transpose (the required square matrix)
Output : The tridagonal form of the matrix
'''

house_ratings = np.dot(ratings,ratings.T) 
dimension = house_ratings.shape[0]
v = [0.0] * dimension
u = [0.0] * dimension
z = [0.0] * dimension
for k in range(0,dimension-2):
	q = 0.0
	alpha = 0.0
	PROD = 0.0
	RSQ = 0.0
	for j in range(k,dimension):
		q = q + house_ratings[j][k]**2

	if house_ratings[k+1][k] == 0 :
		alpha = -(q**0.5)
	else:
		alpha = -(((q**0.5)*house_ratings[k+1][k])/(abs(house_ratings[k+1][k])))

	RSQ = (alpha**2) - alpha*(house_ratings[k+1][k])
	
	v[k] = 0
	v[k+1] = house_ratings[k+1][k] - alpha
	for j in range(k+2,dimension):
		v[j] = house_ratings[j][k]

	for j in range(k,dimension):
		for s in range(k+1,dimension):
			u[j] = u[j] + house_ratings[j][s]*v[s]
		u[j] = (1/RSQ)*u[j]

	for s in range(k+1,dimension):
		PROD = PROD + v[s]*u[s]
	print PROD
	for j in range(k,dimension):
		z[j] = u[j] - (PROD/(2*RSQ))*v[j]

	for l in range(k+1,dimension-1):
		for j in range(l+1,dimension):
			house_ratings[j][l] = house_ratings[j][l] - v[l]*z[j] - v[j]*z[l]
			house_ratings[l][j] = house_ratings[j][l]
		house_ratings[l][l] = house_ratings[l][l] - 2*v[l]*z[l]

	house_ratings[dimension-1][dimension-1] = house_ratings[dimension-1][dimension-1] - 2*v[dimension-1]*z[dimension-1]

	for j in range(k+2,dimension):
		house_ratings[k][j] = 0
		house_ratings[j][k] = 0

	house_ratings[k+1][k] = house_ratings[k+1][k] - v[k+1]*z[k]
	house_ratings[k][k+1] = house_ratings[k][k+1]

'''
QR DECOMPOSITION
Eigen Values of a given matrix A(house_ratings) which is in its tridiagonal form
INPUT : dimension, Tolerance (TOL), maximum number of iterations
OUTPUT : Eigen values of A (house_ratings)
'''

copy_dimension = dimension
diagonal = []
subdiagonal = []
subdiagonal.append(0)
for i in range(0,dimension):
	diagonal.append(house_ratings[i][i])
for i in range(1,dimension):
	subdiagonal.append(house_ratings[i][i-1])
Lambda = []


def QR_Decomposition(diagonal,subdiagonal,dimension):
	global Lambda
	c = [0.0]*dimension
	d = [0.0]*dimension
	x = [0.0]*dimension
	y = [0.0]*dimension
	q = [0.0]*dimension
	s = [0.0]*dimension
	r = [0.0]*dimension
	sigmas= [0.0]*dimension
	z = [0.0]*dimension
	M = 20
	TOL = 0.0001
	k = 0
	SHIFT = 0
	while k<=M:
		if abs(subdiagonal[dimension-1])<=TOL:
			_lambda = diagonal[dimension-1] + SHIFT
			Lambda.append(_lambda)
			dimension = dimension - 1

		if abs(subdiagonal[1])<=TOL:
			_lambda = diagonal[0] + SHIFT
			Lambda.append(_lambda)
			dimension = dimension - 1
			for j in range(0,dimension):
				diagonal[j] = diagonal[j+1]
				subdiagonal[j] = subdiagonal[j+1]			
		subdiagonal[0] = 0

		if dimension == 0 : break

		if dimension == 1 :
			_lambda = diagonal[0] + SHIFT
			Lambda.append(_lambda)
			break

		for j in range(2,dimension-1):
			if subdiagonal[j-1] <= TOL :
				QR_Decomposition(diagonal[0:j-1],subdiagonal[1:j-1],dimension)
				QR_Decomposition(diagonal[j-1:dimension],subdiagonal[j-1:dimension-1],dimension)
				break

		B = -(diagonal[dimension-2]+diagonal[dimension-1])
		C = diagonal[dimension-1]*diagonal[dimension-2] - (subdiagonal[dimension-2])**2
		D = (B**2 - 4*C) ** 0.5

		mew1 = 0.0
		mew2 = 0.0 

		if B > 0 :
			mew1 = (-2*C)/(B+D)
			mew2 = -(B+D)/2
		else:
			mew1 = (D-B)/2
			mew2 = 2*C/(D-B)

		if dimension == 2 :
			lambda1 = mew1 + SHIFT
			lambda2 = mew2 + SHIFT
			Lambda.append(lambda1)
			Lambda.append(lambda2)
			break
		
		sigma = 0
		minimum = min(abs(mew1,diagonal[dimension-1]),abs(mew2,diagonal[dimension-1]))
		if minimum < 0:
			sigma = diagonal[dimension-1] - minimum
		else:
			sigma = diagonal[dimension-1] + minimum
		

		SHIFT = SHIFT + sigma

		for j in range(0,dimension):
			d[j] = diagonal[j] - sigma

		x[0] = d[0]
		y[0] = subdiagonal[0]

		for j in range(1,dimension):
			z[j-1] = ((x[j-1])**2+(subdiagonal[j-2])**2)**0.5
			c[j] = x[j-1] / z[j-1]
			sigmas[j] = subdiagonal[j-2]/z[j-1]
			q[j-1] = c[j]*y[j-1] + s[j]*d[j]
			x[j] = -sigmas[j]*y[j-1] + c[j]*d[j]
			if j != dimension:
				r[j-1] = sigmas[j]*subdiagonal[j-1]
				y[j] =c[j]*subdiagonal[j-1]

			diagonal[0] = sigmas[1]*q[0] + c[1]*z[0]
			subdiagonal[0] = sigmas[1]*z[1]

		for j in range(2,dimension-1):
			diagonal[j] = sigmas[j+1]*q[j] + c[j]*c[j+1]*z[j]
			subdiagonal[j-1] = sigmas[j+1]*z[j+1]

		diagonal[dimension-1] = c[dimension-1]*z[dimension-1]

		k = k + 1


QR_Decomposition(diagonal,subdiagonal,dimension)
print Lambda