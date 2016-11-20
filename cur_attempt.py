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
from single_iter_svd import svd

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

def calc_length(matrix):
	total = 0
	for i in xrange(len(matrix)):
		for j in xrange(len(matrix[i])):
			total = total + matrix[i][j]**2

	return total

############################################################################################################

def selection(matrix):

	matrix = matrix.tolist()	
	rows_selected = []
	prob = [0]*len(matrix)
	total = calc_length(matrix)
	compact_matrix = []
	np.random.seed(777)
	
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

############################################################################################################

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
print calc_error(final_matrix.tolist())