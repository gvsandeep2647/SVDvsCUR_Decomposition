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
from common import handle_input, calc_error, print_matrix
from svd import svd

ratings = handle_input("ratings.txt")

start_time  = time.time()

U,sigma,V = svd(ratings)

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
print "\nPrinting the final matrix got by multiplying U, sigma and V:"
print final_matrix
final_matrix = final_matrix.tolist()
error = calc_error(ratings,final_matrix)
print "\nPrinting the frobenius error:"
print error

print " ************* Execution Time : ************* "
print "--- %s seconds ---" %(time.time() - start_time)