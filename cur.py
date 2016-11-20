import numpy as np
import math
import random
def columnselect(A,c,k):
    U,S,V = np.linalg.svd(A,full_matrices = False)
    dimension = A.shape
    a = V.shape
    p = []
    #print a
    for i in xrange(a[0]):
        p.append(sum((V[i,:k+1]**2))/k)
    #print p
    
    C = np.zeros((dimension[0],c))
    list1 = [i for i in xrange(dimension[1])]
    #print list1
    for t in xrange(c):
        j = random.choice(list1)
        C[:,t] = A[:,j]/(((c**2) * p[j])**0.5)
    return C

'''
	for dummy data
'''

A = np.array([[1,2,3],[2,3,4],[3,4,5]])
c = 2
r = 2
k = 3

C = columnselect(A,c,k)
B = A.transpose()
R = columnselect(B,r,k)
R = R.transpose()
U = np.dot(np.linalg.pinv(C),np.dot(A,np.linalg.pinv(R)))
final = np.dot(C,np.dot(U,R))
print final

'''
	For test.txt
'''
input_file = open("test.txt","r")
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
    
print ratings

c = 5
r = 4
k = 3
C = columnselect(ratings,c,k)
B = ratings.transpose()
R = columnselect(B,r,k)
R = R.transpose()
U = np.dot(np.linalg.pinv(C),np.dot(ratings,np.linalg.pinv(R)))
final = np.dot(C,np.dot(U,R))
print final