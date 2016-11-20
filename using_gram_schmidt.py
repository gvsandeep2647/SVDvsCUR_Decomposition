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

print "Error Calculated Using Inbuilt SVD Package :",calc_error(ratings_svd) #IDEAL ERROR
print

############################################################################################################
def eigen_pairs(matrix):
	
	'''
	FINDING THE SIGNIFICANT EIGEN_VALUES AND EIGEN_VECTORS
	Input : A Matrix
	Output : A dicitonary with keys as eigen values and value as the corressponding eigen vector
	'''

	eigen_values,eigen_vectors = LA.eig(matrix)
	eigen_pairs = {}
	for i in range(0,len(eigen_values)):
		eigen_pairs[eigen_values[i]] = eigen_vectors[:,i]

	eigen_values = sorted(eigen_values)

	final_eigen_pairs = {}
	for j in eigen_values:
		final_eigen_pairs[round(j.real,2)] =  eigen_pairs[j].real

	return final_eigen_pairs

############################################################################################################

def orthonormalize(arr):
    arr = arr.T
    n,m = arr.shape
    ret = np.zeros((n,m))
    ret[0] = arr[0]
    ret[0] = ret[0]/LA.norm(ret[0])
    for i in xrange(1,n):
        ret[i] = arr[i]
        for j in xrange(i):
            x1 = np.dot(ret[j],ret[j])
            x2 = np.dot(arr[i],ret[j])
            rat = x2/x1
            ret[i] = ret[i]-(rat*ret[j])
        ret[i] = ret[i]/np.linalg.norm(ret[i])
    ret = ret.T
    return ret

#############################################################################################################

for_U = eigen_pairs(np.dot(ratings,ratings.T))
for_V = eigen_pairs(np.dot(ratings.T,ratings))


eigen_values = []
for j in for_U:
	if abs(j) !=0 :
		eigen_values.append(round(j,2))
eigen_values = sorted(eigen_values)[::-1]
U = []
for i in range(0,len(eigen_values)):
	U.append(for_U[eigen_values[i]])

U = np.matrix(U)
print U
U = orthonormalize(U)
print U

V = []
for i in range(0,len(eigen_values)):
	V.append(for_U[eigen_values[i]])

V = np.matrix(V)
V = orthonormalize(V.T)

sigma = np.zeros((len(eigen_values),len(eigen_values)))
for i in xrange(len(eigen_values)):
	sigma[i][i] = eigen_values[i]**0.5

final_matrix = np.dot(U,np.dot(sigma,V))
print final_matrix
print calc_error(final_matrix)