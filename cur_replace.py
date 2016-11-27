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
import time
from numpy import linalg as LA
from svd import svd
from common import handle_input, calc_error


def calc_length(matrix):
	"""
	The Square sum of the values of the matrix
	"""
	total = 0
	for i in xrange(len(matrix)):
		for j in xrange(len(matrix[i])):
			total = total + matrix[i][j]**2

	return total

def selection(matrix):

	"""
	Input : The matrix of which we have to select random rows
	Output : Randomly selected rows based on the calculated probability distribution. These rows are scaled so as to compensate the fact that they sometimes are selected multiple times. It also returns the indexes of the selected rows
	No of rows selected = rank of the matrix
	Seed for random number generator : 117

	"""

	matrix = matrix.tolist()	
	rows_selected = []
	prob = [0]*len(matrix)
	total = calc_length(matrix)
	compact_matrix = []
	np.random.seed(117)
	
	for i in xrange(len(matrix)):
		row = 0.0
		for j in xrange(len(matrix[i])):
			row = row + matrix[i][j]**2
		prob[i] = row/total

	rank = LA.matrix_rank(matrix)
	rows_selected = np.random.choice(len(matrix), rank, p=prob)

	for j in xrange(len(rows_selected)):
		compact_matrix.append(matrix[rows_selected[j]])
		factor = (rank*prob[rows_selected[j]])**0.5
		for k in matrix[j]:
			k = k / factor
	return compact_matrix,rows_selected

ratings = handle_input("ratings.txt")
start_time = time.time()

R,rows_selected = selection(ratings)
C,columns_selected = selection(ratings.T)

intersection = np.zeros((len(rows_selected),len(columns_selected)))

for i in xrange(len(rows_selected)):
	for j in xrange(len(columns_selected)):
		intersection[i][j] = ratings[rows_selected[i]][columns_selected[j]]

u,sigma,v = svd(intersection)

u = u.T
v = v.T
for j in xrange(len(sigma)):
	if abs(sigma[j][j])!=0:
		sigma[j][j] = 1/ sigma[j][j]

intersection = np.dot(v,np.dot(sigma,u))
C = np.matrix(C)
C = C.T
R = np.matrix(R)

final_matrix = np.dot(C,np.dot(intersection,R))

print final_matrix

final_error =  calc_error(ratings, final_matrix.tolist())

print "\nFrobenius Error Of the CUR Decomposition is : ",final_error

print " \n************* Execution Time : ************* "
print "--- %s seconds ---" %(time.time() - start_time)