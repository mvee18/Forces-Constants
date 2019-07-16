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
num_of_jobs = raw_data.size * 2

second_energy_list_a = [0.00037726010759797646, 1.3377116501089859, 0.7794059200705306, 0.0004889599836133129, 2.4523686801103395, 1.6416705300059675, 0.0003772402124013752, 1.3377116501089859, 0.7794059200705306]
second_energy_list_b = [0.0, 0.0, -0.000109899929157109, 0.0, 0.0, -9.700045211502584e-06, 0.0, 0.0, 0.839248540103199, -1.2260569000943633, -0.7274316999428265, -0.11139000008597577, -0.1118235799424383, -0.8207080598765515, 0.041567169972722695, 0.0, 0.0, 0.0, 0.0, -0.000109899929157109, 0.0, 0.0, -0.951072299955058, 0.0, -1.226056890146765, 0.951072299955058, -0.8207080598765515, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1118235799424383, 0.7274316999428265, -0.8392485300134922]

a = []
b = []

np.asarray(second_energy_list_a)
np.asarray(second_energy_list_b)

for n in second_energy_list_a:
    a.append(n * (0.529177208)**2)

for n in second_energy_list_b:
    b.append(n * (0.529177208)**2)

print(a)
print(b)

x_repeat = []
y_repeat = []

"""
def arrayToList(arr):
    if type(arr) == type(np.array):
        #If the passed type is an ndarray then convert it to a list and
        #recursively convert all nested types
        return arrayToList(arr.tolist())
    else:
        #if item isn't an ndarray leave it as is.
        return arr

pprint(arrayToList(second_energy_list_a))
pprint(arrayToList(second_energy_list_b))
"""

count_global = 0


"""
def x_lines(row):
    global count_global
    for rows in range(row,row+3,1):
        for cols in range(3):
            if rows != cols:
                zero_array[rows,cols] = b[count_global]
                count_global += 1
"""


np.set_printoptions(suppress=True,
   formatter={'float_kind':'{:20.10f}'.format})

zero_array = np.zeros((27,3))

zero_size = zero_array.shape

item_count = 0
doubles = 0
x_list = 0

print(a[0])
print(len(a))
print(len(b))
"""
for rows in range(zero_size[0]):
    for cols in range(zero_size[1]):
        if rows == 0 and cols == 0:
            item_count = 0
        else:
            item_count += 1
        if item_count % 10 == 0:
            zero_array[rows,cols] = a[doubles]
            doubles += 1
        for j in range(3):
            if j > cols:
                print(b[x_list])
                zero_array[rows,j] = b[x_list]
                x_list += 1


"""
print(zero_size)
# The next three lines do not have repetitions
#    if (rows % 9) == 0:
#        x_lines(rows)
#This is a repeat row.
"""
    if rows % 9 != 0:
        for cols in range(3):
            zero_array[rows,cols] = 69
"""


"""
        for item in range(zero_size[1]):
            if item < rows:
                zero_array[rows,cols] = 420
            else:
                zero_array[rows,cols] = second_energy_list_b[count]
                count += 1
"""
print(zero_array)
"""

for rows in range(size[0]):
    print(rows)
    for cols in range(size[1]):
        print(cols)
        for items in range(size[1]):
            if items == cols:
# This is the +[xx,yy,zz] term.
                raw_data[rows,cols] = raw_data[rows,cols] + differential*2
                data = np.column_stack((labels,raw_data))
                print(data)
                raw_data[rows,cols] = reset[rows,cols]
# This is the -[xx,yy,zz] term.
                raw_data[rows,cols] = raw_data[rows,cols] - differential*2
                data = np.column_stack((labels,raw_data))
                print(data)
                raw_data[rows,cols] = reset[rows,cols]

#Vertical distribution of displacements.
        for i in range(size[0]):
            if i > rows:
# X1 and X2...
                print(i)
                raw_data[rows,cols] = raw_data[rows,cols] + differential
                raw_data[i,cols] = raw_data[i,cols] + differential
                data = np.column_stack((labels,raw_data))
                np.savetxt("tmp.txt", data, delimiter=" ", fmt='%s')
                print(data)
                raw_data[rows,cols] = reset[rows,cols]
                raw_data[i,cols] = reset[i,cols]
#-X1 and -X2
                raw_data[rows,cols] = raw_data[rows,cols] - differential
                raw_data[i,cols] = raw_data[i,cols] - differential
                data = np.column_stack((labels,raw_data))
                np.savetxt("tmp2.txt", data, delimiter=" ", fmt='%s')
                print(data)
                raw_data[rows,cols] = reset[rows,cols]
                raw_data[i,cols] = reset[i,cols]
# -X1 and X2
                raw_data[rows,cols] = raw_data[rows,cols] - differential
                raw_data[i,cols] = raw_data[i,cols] + differential
                data = np.column_stack((labels,raw_data))
                np.savetxt("tmp3.txt", data, delimiter=" ", fmt='%s')
                print(data)
                raw_data[rows,cols] = reset[rows,cols]
                raw_data[i,cols] = reset[i,cols]
# X1 and -X2.
                raw_data[rows,cols] = raw_data[rows,cols] + differential
                raw_data[i,cols] = raw_data[i,cols] - differential
                data = np.column_stack((labels,raw_data))
                np.savetxt("tmp4.txt", data, delimiter=" ", fmt='%s')
                print(data)
                raw_data[rows,cols] = reset[rows,cols]
                raw_data[i,cols] = reset[i,cols]
            for j in range(size[1]):
                if j > cols:
                    raw_data[rows,cols] = raw_data[rows,cols] + differential
                    raw_data[i,j] = raw_data[i,j] + differential
                    print(raw_data)
                    raw_data[rows,cols] = reset[rows,cols]
                    raw_data[i,j] = reset[i,j]

                    raw_data[rows,cols] = raw_data[rows,cols] - differential
                    raw_data[i,j] = raw_data[i,j] - differential
                    print(raw_data)
                    raw_data[rows,cols] = reset[rows,cols]
                    raw_data[i,j] = reset[i,j]

                    raw_data[rows,cols] = raw_data[rows,cols] - differential
                    raw_data[i,j] = raw_data[i,j] + differential
                    print(raw_data)
                    raw_data[rows,cols] = reset[rows,cols]
                    raw_data[i,j] = reset[i,j]

                    raw_data[rows,cols] = raw_data[rows,cols] + differential
                    raw_data[i,j] = raw_data[i,j] - differential
                    print(raw_data)
                    raw_data[rows,cols] = reset[rows,cols]
                    raw_data[i,j] = reset[i,j]
"""
"""
            elif items > cols:
# These are the ways to arrange two terms together: positives.
                raw_data[rows,cols] = raw_data[rows,cols] + differential
                raw_data[rows,items] = raw_data[rows,items] + differential
                data = np.column_stack((labels,raw_data))
                np.savetxt("tmp.txt", data, delimiter=" ", fmt='%s')
                print(data)
                raw_data[rows,cols] = reset[rows,cols]
                raw_data[rows,items] = reset[rows,items]
# These are the ways to arrange the -,-: negatives.
                raw_data[rows,cols] = raw_data[rows,cols] - differential
                raw_data[rows,items] = raw_data[rows,items] - differential
                data = np.column_stack((labels,raw_data))
                np.savetxt("tmp2.txt", data, delimiter=" ", fmt='%s')
                print(data)
                raw_data[rows,cols] = reset[rows,cols]
                raw_data[rows,items] = reset[rows,items]
# -,+: minusplus
                raw_data[rows,cols] = raw_data[rows,cols] - differential
                raw_data[rows,items] = raw_data[rows,items] + differential
                data = np.column_stack((labels,raw_data))
                np.savetxt("tmp3.txt", data, delimiter=" ", fmt='%s')
                print(data)
                raw_data[rows,cols] = reset[rows,cols]
                raw_data[rows,items] = reset[rows,items]
#+,-: plusminus
                raw_data[rows,cols] = raw_data[rows,cols] + differential
                raw_data[rows,items] = raw_data[rows,items] - differential
                data = np.column_stack((labels,raw_data))
                np.savetxt("tmp4.txt", data, delimiter=" ", fmt='%s')
                print(data)
                raw_data[rows,cols] = reset[rows,cols]
                raw_data[rows,items] = reset[rows,items]
"""

#New Ideas:
number_of_points = (size[0])**4
geom_list = [0,0,0,0]

zero_array = zero_array.astype('object')

for i in range(27):
    for j in range(3):
        zero_array[i,j] = [0,0,0,0]

array = []
for atom1 in range(3):
    coordinate_list1 = []
    for coordinate1 in range(3):
        atom_list1 = []
        for atom2 in range(3):
            coordinate_list2 = []
            for coordinate2 in range(3):
                coordinate_list2.append(coordinate2)
            atom_list1.append(coordinate_list2)
        coordinate_list1.append(atom_list1)
    array.append(coordinate_list1)

array = np.asarray(array)

shapefour = array.shape
print(shapefour)

def convert(list):
    s = [str(i) for i in list]
    res = int("".join(s))
    return(res)

def manipulate_geometry(a1,c1,a2,c2):


for i in range(shapefour[0]):
    for j in range(shapefour[1]):
        Found = False
        for k in range(shapefour[2]):
            for l in range(shapefour[3]):
                if i == k and j == l:
                    array[i,j,k,l] = 7
                    value = (i,j,k,l)
                    res = convert(value)
                    Found = True
                elif Found:
                    comparison_list = (i,j,k,l)
                    comparevalue = convert(comparison_list)
                    if comparevalue > res:
                        array[i,j,k,l] = 777
                        print(comparevalue, res)
                    else:
                        array[i,j,k,l] = 0
                else:
                    array[i,j,k,l] = 0

print(array)
