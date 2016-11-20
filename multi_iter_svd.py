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
from common import handle_input, calc_error
from svd import eigen_pairs

'''
Calculating the matrices U,V and Sigma based on the eigen values returned by the numpy.linalg.eig function
'''
ratings = handle_input("ratings.txt")


start_time = time.time()

for_U = eigen_pairs(np.dot(ratings,ratings.T))
for_V = eigen_pairs(np.dot(ratings.T,ratings))

eigen_values = []
for j in for_U:
	if abs(j) !=0 :
		eigen_values.append(round(j,2))
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

eigen_values = sorted(eigen_values)[::-1]
U = np.zeros((len(eigen_values),len(for_U[eigen_values[0]])))

for i in xrange(len(eigen_values)):
	for j in xrange(len(for_U[eigen_values[i]])):
		U[i][j] = for_U[eigen_values[i]][j]

U = U.T

V = np.zeros((len(eigen_values),len(for_V[eigen_values[0]])))

for i in xrange(len(eigen_values)):
	for j in xrange(len(for_V[eigen_values[i]])):
		V[i][j] = for_V[eigen_values[i]][j]

sigma = np.zeros((len(eigen_values),len(eigen_values)))
for i in range(len(sigma)):
	sigma[i][i] = eigen_values[i]**0.5

###############################################################################################################

'''
Here we are trying to find the minimum possible frobenius error by iterating through all the possible values of eigen vectors
'''


final_U = np.zeros((len(eigen_values),len(for_U[eigen_values[0]])))
final_V = np.zeros((len(eigen_values),len(for_V[eigen_values[0]])))
final_matrix = np.dot(U,np.dot(sigma,V))
temp_error = calc_error(ratings, final_matrix)
final_error = 0.0

for i in xrange(len(U[0])):
	print "Running U for column ",i
	U[:,i] = U[:,i]*-1
	temp_matrix = np.dot(U,np.dot(sigma,V))
	iter_error = calc_error(ratings, temp_matrix)
	if iter_error < temp_error:
		temp_error = iter_error
		final_error = iter_error
		final_U = U
		final_matrix = temp_matrix
		print "Currently,the best possible matrix \n",final_matrix
		print "Currently,the best possible error ", final_error
	U[:,i] = U[:,i]*-1

for i in xrange(len(V)):
	print "Running V for row ",i
	V[i] = V[i]*-1
	temp_matrix = np.dot(U,np.dot(sigma,V))
	iter_error = calc_error(ratings, temp_matrix)
	if iter_error < temp_error:
		temp_error = iter_error
		final_error = iter_error
		final_V = V
		final_matrix = temp_matrix	
		print "Currently,the best possible matrix \n" ,final_matrix
		print "Currently,the best possible error ", final_error
	V[i] = V[i]*-1

for i in xrange(len(U[0])):
	U[:,i] = U[:,i] * -1
	for j in xrange(len(V)):
		print "Running U for column ",i," V for row ",j
		V[j] = V[j]*-1
		iter_error = calc_error(ratings, np.dot(U,np.dot(sigma,V)))
		if iter_error < temp_error :
			final_U = U
			final_V = V
			final_error = iter_error
			temp_error = final_error
			final_matrix = np.dot(final_U,np.dot(sigma,final_V))
			print "Currently,the best possible matrix \n",final_matrix
			print "Currently,the best possible error ",final_error
		V[j] = V[j]*-1
	U[:,i] = U[:,i]*-1

print "Frobenius Error Of the SVD Decomposition is : ",final_error
print "The matrix obtained by multiplying U , sigma and V' :"

for i in xrange(len(final_matrix)):
	for j in xrange(len(final_matrix[i])):
		final_matrix[i][j] = round(final_matrix[i][j],2)

print final_matrix
print " ************* Execution Time : ************* "
print "--- %s seconds ---" %(time.time() - start_time)