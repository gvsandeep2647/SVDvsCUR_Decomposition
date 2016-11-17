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

'''
FINDING THE SIGNIFICANT EIGEN_VALUES AND EIGEN_VECTORS
Input : 
'''

def eigen_pairs(matrix):
	for_U = matrix
	eigen_values,eigen_vectors = LA.eig(for_U)
	eigen_pairs = {}
	for i in range(0,len(eigen_values)):
		eigen_pairs[eigen_values[i]] = eigen_vectors[:,i]

	eigen_values = sorted(eigen_values)
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

	final_eigen_pairs = {}
	for j in eigen_values:
		final_eigen_pairs[j] = eigen_pairs[j]

	return final_eigen_pairs

for_U = eigen_pairs(np.dot(ratings,ratings.T))
for_V = eigen_pairs(np.dot(ratings.T,ratings))

eigen_values = []
for j in for_U:
	eigen_values.append(j)

eigen_values = sorted(eigen_values)