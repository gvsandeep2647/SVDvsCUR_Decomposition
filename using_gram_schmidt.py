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

ratings = handle_input("ratings.txt")

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
def print_matrix(matrix):

	'''
	UTITLITY FUNCTION TO PRINT A MATRIX
	Input : A matrix
	Output: prints the matrix onto the console 
	'''
	for i in xrange(len(matrix)):
		for j in xrange(len(matrix[i])):
			print matrix[i][j],
		print "\n"

############################################################################################################
'''
CALCULATING THE SINGULAR VALUE DECOMPOSTION BY COMPUTING THE EIGENVALUES AND EIGENVECTORS
'''

for_U = eigen_pairs(np.dot(ratings,ratings.T))
for_V = eigen_pairs(np.dot(ratings.T,ratings))

eigen_values = []
for j in for_U:
	if abs(j) !=0 :
		eigen_values.append(round(j,2))
eigen_values = sorted(eigen_values)[::-1]

U = np.zeros((len(for_U[eigen_values[0]]),len(eigen_values)))
V = np.zeros((len(for_V[eigen_values[0]]),len(eigen_values)))

for j in xrange(len(eigen_values)):
	for i in xrange(len(for_U[eigen_values[j]])):
		U[i][j] = for_U[eigen_values[j]][i]
	for i in xrange(len(for_V[eigen_values[j]])):
		V[i][j] = for_V[eigen_values[j]][i]

V = V.T

sigma = np.zeros((len(eigen_values),len(eigen_values)))
for i in xrange(len(eigen_values)):
	sigma[i][i] = eigen_values[i]**0.5


final_matrix = (np.dot(U,np.dot(sigma,V)))

for i in xrange(len(final_matrix)):
	for j in xrange(len(final_matrix[i])):
		final_matrix[i][j] = round(final_matrix[i][j],2)

print "Printing matrix U:"
print U
print "\nPrinting matrix sigma:"
print sigma
print "\nPrinting matrix V:"
print V
print "\nPrinting the final matrix got by multiplying U,sigma and V:"
print final_matrix
final_matrix = final_matrix.tolist()
min_error = calc_error(final_matrix)
print "\nPrinting the frobenius error:"
print min_error



#print final_matrix
#print calc_error(final_matrix)