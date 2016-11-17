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
############################################################################################################

ratings = handle_input("test1.txt")


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
	

	"""	
	neg_energy = 0.0
	energy = 0.0

	for j in eigen_values:
		energy = energy + j

	for j in xrange(len(eigen_values)):
		neg_energy = neg_energy + eigen_values[j]
		if neg_energy/energy < 0.099:
			eigen_values[j] = 0.0

	for j in eigen_values[:]:
		if j == 0:
			eigen_values.remove(j)
	"""

	final_eigen_pairs = {}
	for j in eigen_values:
		final_eigen_pairs[round(j.real,2)] =  eigen_pairs[j].real

	return final_eigen_pairs
############################################################################################################

#for_U = eigen_pairs(np.dot(ratings,ratings.T))
#for_V = eigen_pairs(np.dot(ratings.T,ratings))

def basicQR(A):
	u = np.zeros((len(A),len(A[0])))
	for i in xrange(len(A)):
		u[i][i] = 1
	for k in xrange(100):
		q,r = LA.qr(A)
		A = np.dot(r,q)
		u = np.dot(u,q)
	ev = []
	ep = {}
	for i in xrange(len(A)):
		ev.append(round(A[i][i],2))
	for i in xrange(len(ev)):
		ep[ev[i]] = u[:,i]
	return ep

for_U = basicQR(np.dot(ratings, ratings.T))
for_V = basicQR(np.dot(ratings.T,ratings))

eigen_values = []
for j in for_U:
	if j !=0 :
		eigen_values.append(j)

eigen_values = sorted(eigen_values)[::-1]

sigma  = np.zeros((len(eigen_values),len(eigen_values)))
U = np.zeros((len(for_U[eigen_values[0]]),len(eigen_values)))
V = np.zeros((len(for_V[eigen_values[0]]),len(eigen_values)))


for j in xrange(len(eigen_values)):
	for i in xrange(len(for_U[eigen_values[0]])):
		U[i][j] = for_U[eigen_values[j]][i]
	for i in xrange(len(for_V[eigen_values[0]])):
		V[i][j] = for_V[eigen_values[j]][i]
	sigma[j][j] = eigen_values[j]**0.5

def dot_product(temp1, temp2):
	temp_answer = 0.0
	for j in xrange(len(temp1)) :
		temp_answer = temp_answer + temp1[j]*temp2[j]
	temp_answer = abs(temp_answer)**0.5
	return temp_answer

def gram_schmidt(matrix):
	degree_vector = len(matrix)
	no_of_vectors = len(matrix[0])
	U = np.zeros((degree_vector,no_of_vectors))
	U[:,0] = matrix[:,0]/dot_product(matrix[:,0],matrix[:,0])
	for i in range(1,no_of_vectors):
		U[:,i] = matrix[:,i]
		for j in range(0,i-1):
			U[:,i] = U[:,i] - (dot_product(U[:,i],U[:,j]))*U[:,j]
		U[:,i] = U[:,i]/dot_product(U[:,i],U[:,i])
	return U

def usingQR(A):
	q,r = LA.qr(A)
	s = np.zeros((len(r),len(r[0])))
	for i in xrange(len(r)):
		if r[i][i]>0:
			s[i][i] = 1
		elif r[i][i]<0:
			s[i][i] = -1
	b = np.dot(q,s)
	print b	


V=V.T
final_matrix =  np.dot(U,np.dot(sigma,V))
final_matrix = final_matrix.tolist()

#print final_matrix
print calc_error(final_matrix)