import numpy as np
import os
import subprocess

reset = np.genfromtxt('geom.xyz', skip_header=1, usecols=(1,2,3))
raw_data = np.genfromtxt('geom.xyz', skip_header=1, usecols=(1,2,3))
labels = np.genfromtxt('geom.xyz', skip_header=1, dtype=str, usecols=0)

differential = 0.005
nn = 1

size = raw_data.shape
num_of_jobs = raw_data.size * 2

second_energy_list_a = [0.00037726010759797646, 1.3377116501089859, 0.7794059200705306, 0.0004889599836133129, 2.4523686801103395, 1.6416705300059675, 0.0003772402124013752, 1.3377116501089859, 0.7794059200705306]
second_energy_list_b = [0.0, 0.0, -0.000109899929157109, -9.700045211502584e-06, 0.839248540103199, -1.2260569000943633, -0.11139000008597577, -0.8207080598765515, 0.041567169972722695, 0.0, 0.0, -0.000109899929157109, 0.0, -1.226056890146765, -0.8207080598765515, 0.0, 0.0, -0.8392485300134922]

np.asarray(second_energy_list_a)
np.asarray(second_energy_list_b)

for n in range(len(second_energy_list_a)):
    second_energy_list_a[n] = (second_energy_list_a[n] * (0.529177208)**2)

for n in range(len(second_energy_list_b)):
    second_energy_list_b[n] = (second_energy_list_b[n] * (0.529177208)**2)

print(second_energy_list_a)
print(second_energy_list_b)

zero_array = np.zeros((27,3))
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
                if j > cols and i != 0:
                    raw_data[rows,cols] = raw_data[rows,cols] + differential
                    raw_data[i,j] = raw_data[i,j] + differential
                    print(raw_data)
                    raw_data[rows,cols] = reset[rows,cols]
                    raw_data[i,j] = reset[i,j]
"""
