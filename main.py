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

input_file = open("ratings.txt","r")
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
Caluclating the Frobenius Error obtained by using the inbuilt SVD package of Python
"""
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
Implemntation of SVD
"""
prod_for_U = np.dot(ratings,ratings.T)  # First step for finding the matrix U is to find A*A.Transpose