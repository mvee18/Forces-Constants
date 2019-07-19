import numpy as np
import os
import subprocess
from pprint import pprint

reset = np.genfromtxt('geom.xyz', skip_header=1, usecols=(1,2,3))
raw_data = np.genfromtxt('geom.xyz', skip_header=1, usecols=(1,2,3))
labels = np.genfromtxt('geom.xyz', skip_header=1, dtype=str, usecols=0)

differential = 0.005
nn = 1

size = raw_data.shape
num_of_jobs = raw_data.size

third_list = []

def determine_atom(row,atom_number,item):

    if int(third_array[row, atom_number, item]) % 3 == 0:
        third_array[row,atom_number,item] = 0
    elif int(third_array[row, atom_number,item]) % 3 == 1:
        third_array[row,atom_number,item] = 1
    elif int(third_array[row,atom_number,item]) % 3 == 2:
        third_array[row,atom_number,item] = 2

def determine_coordinate(row,coordinate_number,item):
    if int(third_array[row, coordinate_number,item]) // 3 == 0:
        third_array[row,coordinate_number,item] = 0
    elif int(third_array[row, coordinate_number,item]) // 3 == 1:
        third_array[row,coordinate_number,item] = 1
    elif int(third_array[row,coordinate_number,item]) // 3 == 2:
        third_array[row,coordinate_number,item] = 2

#You can also turn this into X,Y,Z instead of 0,1,2, but I think it's easier this way since you can use all ints.

for i in range(num_of_jobs):
    for j in range(num_of_jobs):
        for k in range(num_of_jobs):
            if j <= i and k <= j:
                third_list.append(((i,i),(j,j),(k,k)))

third_array = np.asarray(third_list)

third_array_shape = third_array.shape
print(third_array_shape)

third_array = third_array.astype('object')

print(third_array[0])

for row in range(third_array_shape[0]):
    for col in range(third_array_shape[1]):
        pair = 0
        if pair == 0:
            determine_atom(row,col,pair)
    for col in range(third_array_shape[1]):
        pair = 1
        if pair == 1:
            third_array[row,col,1] = int(third_array[row,col,1])
            determine_coordinate(row,col,1)

print(third_array)


def third_geometries():
    for row in range(third_array_shape[0]):
        for col in range(0,third_array_shape[1],2):
            third_array[row,col] = third_atom
            third_array[row,col+1] = third_coordinate
            raw_data
