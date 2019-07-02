import os
import numpy as np

differential = 0.05

reset = np.genfromtxt('geom.xyz', skip_header=1, dtype=float, usecols=(1,2,3))
raw_data = np.genfromtxt('geom.xyz', skip_header=1, dtype=float, usecols=(1,2,3))
labels = np.genfromtxt('geom.xyz', skip_header=1, dtype=str, usecols=0)

size = raw_data.shape

print(raw_data)

def calc_first_deriative(epos,eneg):
    first_energy = (float(epos) - float(eneg))/(2*differential)
    print(first_energy)
    return

def calc_first_geometry(coordinate):
    print(coordinate)
    output_pos = coordinate + differential
    output_neg = coordinate + differential
    return

for rows in range(size[0]):
    for cols in range(size[1]):
        calc_first_geometry(raw_data[rows,cols])
        raw_data[]
        print(raw_data)
        raw_data = reset
