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

def double_third_terms(zipped,paired,unpaired):
    print(paired,unpaired)
    raw_data[zipped[paired]] = raw_data[zipped[paired]] + 2 * differential
    raw_data[zipped[unpaired]] = raw_data[zipped[unpaired]] + differential
    print(raw_data)
    raw_data[:] = reset[:]

    raw_data[zipped[unpaired]] = raw_data[zipped[unpaired]] + differential
    print(raw_data)
    raw_data[:] = reset[:]

    raw_data[zipped[paired]] = raw_data[zipped[paired]] - 2 * differential
    raw_data[zipped[unpaired]] = raw_data[zipped[unpaired]] - differential
    print(raw_data)
    raw_data[:] = reset[:]

    raw_data[zipped[paired]] = raw_data[zipped[paired]] + 2 * differential
    raw_data[zipped[unpaired]] = raw_data[zipped[unpaired]] - differential
    print(raw_data)
    raw_data[:] = reset[:]

    raw_data[zipped[unpaired]] = raw_data[zipped[unpaired]] - differential
    print(raw_data)
    raw_data[:] = reset[:]

    raw_data[zipped[paired]] = raw_data[zipped[paired]] - 2 * differential
    raw_data[zipped[unpaired]] = raw_data[zipped[unpaired]] - differential
    print(raw_data)
    raw_data[:] = reset[:]

def triple_third_terms(coord1,coord2,coord3,zipped):
    raw_data[zipped[coord1]] = raw_data[zipped[coord1]] + differential
    raw_data[zipped[coord2]] = raw_data[zipped[coord2]] + differential
    raw_data[zipped[coord3]] = raw_data[zipped[coord3]] + differential
    print(raw_data)
    raw_data[:] = reset[:]

    raw_data[zipped[coord1]] = raw_data[zipped[coord1]] + differential
    raw_data[zipped[coord2]] = raw_data[zipped[coord2]] - differential
    raw_data[zipped[coord3]] = raw_data[zipped[coord3]] + differential
    print(raw_data)
    raw_data[:] = reset[:]

    raw_data[zipped[coord1]] = raw_data[zipped[coord1]] - differential
    raw_data[zipped[coord2]] = raw_data[zipped[coord2]] + differential
    raw_data[zipped[coord3]] = raw_data[zipped[coord3]] + differential
    print(raw_data)
    raw_data[:] = reset[:]

    raw_data[zipped[coord1]] = raw_data[zipped[coord1]] - differential
    raw_data[zipped[coord2]] = raw_data[zipped[coord2]] - differential
    raw_data[zipped[coord3]] = raw_data[zipped[coord3]] + differential
    print(raw_data)
    raw_data[:] = reset[:]

    raw_data[zipped[coord1]] = raw_data[zipped[coord1]] + differential
    raw_data[zipped[coord2]] = raw_data[zipped[coord2]] + differential
    raw_data[zipped[coord3]] = raw_data[zipped[coord3]] - differential
    print(raw_data)
    raw_data[:] = reset[:]

    raw_data[zipped[coord1]] = raw_data[zipped[coord1]] + differential
    raw_data[zipped[coord2]] = raw_data[zipped[coord2]] - differential
    raw_data[zipped[coord3]] = raw_data[zipped[coord3]] - differential
    print(raw_data)
    raw_data[:] = reset[:]

    raw_data[zipped[coord1]] = raw_data[zipped[coord1]] - differential
    raw_data[zipped[coord2]] = raw_data[zipped[coord2]] + differential
    raw_data[zipped[coord3]] = raw_data[zipped[coord3]] - differential
    print(raw_data)
    raw_data[:] = reset[:]

    raw_data[zipped[coord1]] = raw_data[zipped[coord1]] - differential
    raw_data[zipped[coord2]] = raw_data[zipped[coord2]] - differential
    raw_data[zipped[coord3]] = raw_data[zipped[coord3]] - differential
    print(raw_data)
    raw_data[:] = reset[:]

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

print(third_array[0])

row_list = []
col_list = []

def third_geometries():
    for i in range(third_array_shape[0]):
        for j in range(third_array_shape[1]):
            row_list.append(third_array[i,j,0])
            col_list.append(third_array[i,j,1])
        zipped = zip(row_list,col_list)
        zipped = list(zipped)
        if zipped[0] == zipped[1] and zipped[1] == zipped[2]:
            print("triple found")
            print(zipped)
            raw_data[zipped[0]] = raw_data[zipped[0]] + 3 * differential
            print(raw_data)
            raw_data[:] = reset[:]

            raw_data[zipped[0]] = raw_data[zipped[0]] - 3*differential
            print(raw_data)
            raw_data[:] = reset[:]

        elif zipped[0] == zipped[1]:
            print("double found")
            print(zipped)
            double_third_terms(zipped,0,2)

        elif zipped[1] == zipped[2]:
            print("double found")
            print(zipped)
            double_third_terms(zipped,1,0)

        elif zipped[0] == zipped[2]:
            print("double found")
            print(zipped)
            double_third_terms(zipped,0,1)

        elif zipped[0] != zipped[1] and zipped[1] != zipped[2]:
            print("single term")
            print(zipped)
            triple_third_terms(0,1,2)

#            print(zipped)
        else:
            print("you dun goofed")
        row_list.clear()
        col_list.clear()
#        for items in zipped:
#            print(items)


third_geometries()
