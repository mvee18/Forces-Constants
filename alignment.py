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

count_global = 0

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

print(zero_size)

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

def manipulate_geometry_first(a1,c1,a2,c2):
    print("no")

def manipulate_geometry_second(a1,c1,a2,c2):
    if a1 == a2 and c1 == c2:
        raw_data[a1,c1] = raw_data[a1,c1] + differential*2
        pos_dif = np.column_stack((labels,raw_data))
        print(pos_dif)

        raw_data[a1,c1] = raw_data[a1,c1] - differential*2
        neg_dif = np.column_stack((labels,raw_data))
        print(neg_dif)
    else:
        raw_data[a1,c1] = raw_data[a1,c1] + differential


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
