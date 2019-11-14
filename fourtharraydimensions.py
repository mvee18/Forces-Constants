import os
import numpy as np
import threading
import subprocess
from threading import Thread
import time

reset = np.genfromtxt('geom.xyz', skip_header=1, usecols=(1,2,3))
raw_data = np.genfromtxt('geom.xyz', skip_header=1, usecols=(1,2,3))
labels = np.genfromtxt('geom.xyz', skip_header=1, dtype=str, usecols=0)
memory_list = [50]

# This outputs as (rows,cols):
size = raw_data.shape
num_of_jobs = raw_data.size

print(size)

def determinefourthsize(size):
    total_points_tally = []

    size_of_data = size
    for i in range(1,size_of_data+1,1):
        for j in range(i):
            for k in range(j+1):
                total_points_tally.append(k+1)

    total_points = int(sum(total_points_tally))
    print(total_points)
    return total_points//3

np.set_printoptions(suppress=True,
   formatter={'float_kind':'{:20.10f}'.format})

print(determinefourthsize(num_of_jobs))

"""
array = np.reshape(third_energy_array,(determinethirdsize(num_of_jobs),3))
print(array)

e = open('fort.40','w+')

#Generalize this.
np.savetxt('fort.40',array,header='    3   495',fmt='%20.10f',comments='')
e.close()
"""
