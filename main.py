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

def handle_input(filename):

	'''
	TAKING INPUT AND FORMING A MATRIX OUT OF IT
	Input : A text file containing lines of the format "USER_ID ITEM_ID RATING"
	Output : A matrix which stores this data 
	'''

	input_file = open(filename,"r")
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

	return ratings

ratings = handle_input("test.txt")

############################################################################################################

def calc_error(ratings_svd):
	
	'''
	Caluclating the Frobenius Error
	'''
	
	error = 0

	for i in range(0,len(ratings)):
		for j in range(0,len(ratings[i])):
			error = error + (ratings[i][j]-ratings_svd[i][j])**2

	error = math.sqrt(error)
	return error

############################################################################################################

'''
USING THE BUILT IN SVD FUNCTION OF PYHTON LANGUAGE (numpy.linalg.svd(matrix))
'''
U,sigma,V = LA.svd(ratings,full_matrices=False)
final_sigma = np.zeros((len(sigma),len(sigma)))
for i in range(0,len(sigma)):
	final_sigma[i][i] = sigma[i]


ratings_svd = np.dot(U, np.dot(final_sigma, V))

print calc_error(ratings_svd) #IDEAL ERROR


def eigen_pairs(matrix):
	
	'''
	FINDING THE SIGNIFICANT EIGEN_VALUES AND EIGEN_VECTORS
	Input : A Matrix
	Output : A dicitonary with keys as eigen values and value as the corressponding eigen vector
	'''

	for_U = matrix
	eigen_values,eigen_vectors = LA.eig(for_U)
	eigen_pairs = {}
	for i in range(0,len(eigen_values)):
		eigen_pairs[eigen_values[i]] = eigen_vectors[:,i]

	eigen_values = sorted(eigen_values)

	final_eigen_pairs = {}
	for j in eigen_values:
		final_eigen_pairs[round(j.real,2)] =  eigen_pairs[j].real

	return final_eigen_pairs

############################################################################################################

def basicQR(A):
	u = np.zeros((len(A),len(A[0])))
	for i in xrange(len(A)):
		u[i][i] = 1
	for k in xrange(100):
		print k
		q,r = LA.qr(A)
		A = np.dot(r,q)
		u = np.dot(u,q)
	ev = []
	ep = {}
	for i in xrange(len(A)):
		ev.append(round(A[i][i],2))
		ep[ev[i]] = u[:,i]
	return ep

############################################################################################################


eigen_values = []
eigen_values_V = []
for j in for_U:
	if abs(j) !=0 :
		eigen_values.append(j)

for j in for_V:
	if j!=0:
		eigen_values_V.append(j)


eigen_values = sorted(eigen_values)[::-1]
eigen_values_V = sorted(eigen_values_V)[::-1]
print eigen_values
print eigen_values_V	

sigma  = np.zeros((len(eigen_values),len(eigen_values)))
U = np.zeros((len(for_U[eigen_values[0]]),len(eigen_values)))
V = np.zeros((len(for_V[eigen_values[0]]),len(eigen_values)))

for j in xrange(len(eigen_values)):
	if(eigen_values[j] != eigen_values_V[j]):
		if eigen_values[j] > eigen_values_V[j]:
			sigma[j][j] = eigen_values[j]**0.5
		else :
			sigma[j][j] = eigen_values_V[j]**0.5
	else:
		sigma[j][j] = eigen_values[j]**0.5
	for i in xrange(len(for_U[eigen_values[0]])):
		U[i][j] = for_U[eigen_values[j]][i]
	for i in xrange(len(for_V[eigen_values_V[0]])):
		V[i][j] = for_V[eigen_values_V[j]][i]
	

V=V.T
final_matrix =  np.dot(U,np.dot(sigma,V))
final_matrix = final_matrix.tolist()

print calc_error(final_matrix)