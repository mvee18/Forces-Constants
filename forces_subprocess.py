import os
import numpy as np
import threading
import subprocess

differential = 0.005

reset = np.genfromtxt('geom.xyz', skip_header=1, usecols=(1,2,3))
raw_data = np.genfromtxt('geom.xyz', skip_header=1, usecols=(1,2,3))
labels = np.genfromtxt('geom.xyz', skip_header=1, dtype=str, usecols=0)
memory_list = [495]

# This outputs as (rows,cols):
size = raw_data.shape
num_of_jobs = raw_data.size * 2
input_list = []
for i in range(num_of_jobs):
    input_list.append(i)

def gen_com(differentialtype):
    for i in range(num_of_jobs):
        temp = open('tmp.txt', 'r')
        f = open("input.com", 'w+')
        f.write("memory,%d,m\n" %memory_list[0])
        f.write("\nnocompress;\n")
        f.write("geomtyp=xyz\n")
        f.write("angstrom\n")
        f.write("geometry={\n")
        f.write(temp.read())
        f.write("}")
        f.write("\n")
        f.write("basis=cc-pVTZ-F12\n")
        f.write("set,charge=0\n")
        f.write("set,spin=0\n")
        f.write("hf\n")
        f.write("{CCSD(T)-F12}")
        f.close()
        temp.close()

# First derivatives.

def first_derivative():
    for i in range(len(positives)):
        first_energy = ((float(positives[i]) - float(negatives[i]))/(2*differential))
        if i % 3 == 0:
            print("d/dx:")
            print(first_energy)
        elif i % 3 == 1:
            print("d/dy:")
            print(first_energy)
        elif i % 3 == 2:
            print("d/dz")
            print(first_energy)

positives = []
negatives = []
minusplus = []
plusminus = []

def extract_energy(posorneg):
    if posorneg == "pos_dif":
        sub_job()
        zz = open("input.out", 'r')
        zzz = zz.readlines()
        for line in zzz:
            if "!CCSD(T)-F12b total energy" in line:
                line = line.split()
                positives.append(line[3])
    elif posorneg == "neg_dif":
        sub_job()
        zz = open("input.out", 'r')
        zzz = zz.readlines()
        for line in zzz:
            if "!CCSD(T)-F12b total energy" in line:
                line = line.split()
                negatives.append(line[3])
    elif posorneg == "minusplus":
        sub_job()
        zz = open("input.out", 'r')
        zzz = zz.readlines()
        for line in zzz:
            if "!CCSD(T)-F12b total energy" in line:
                line = line.split()
                minusplus.append(line[3])
    elif posorneg == "plusminus":
        sub_job()
        zz = open("input.out", 'r')
        zzz = zz.readlines()
        for line in zzz:
            if "!CCSD(T)-F12b total energy" in line:
                line = line.split()
                plusminus.append(line[3])

def sub_job():
    subprocess.call("mpiexec molpro.exe input.com", shell=True)
    return

"""
#After header, we will have to do the submission.
for rows in range(size[0]):
    for cols in range(size[1]):
        raw_data[rows,cols] = raw_data[rows,cols] + differential
        pos_dif = np.column_stack((labels,raw_data))
        np.savetxt("tmp.txt", pos_dif, delimiter=" ", fmt='%s')
        gen_com(pos_dif)
        extract_energy("pos_dif")
        raw_data[rows,cols] = reset[rows,cols]

for i in range(size[0]):
    for cols in range(size[1]):
        raw_data[rows,cols] = raw_data[rows,cols] - differential
        neg_dif = np.column_stack((labels,raw_data))
        np.savetxt("tmp.txt", neg_dif, delimiter=" ", fmt='%s')
        gen_com(neg_dif)
        extract_energy("neg_dif")
        raw_data[rows,cols] = reset[rows,cols]

print(positives)
print(negatives)

positives.clear()
negatives.clear()
"""
# Second derivatives.
# We need the following pairs: [(x1,xn),(y1,yn),(z1.zn),(x1,yn),(x1,zn),(y1,zn)], without repeating.

# I used a triple loop in order to assign a third dimension to the array, which is the item number within the line.
# This keeps track of xyz that the currently [row,col] value needs to be added to.
# If the item # = the col, then they are the same, and the dif needs to be added twice.
# If the item # > col, then it needs to add the two. Iterating this is equivalent to creating the permuations.
# Most significantly, this prevents double counting.

# Redefine lists to help me understand.
a = positives
b = plusminus
c = minusplus
d = negatives

# This is for all ways to add two terms together (+dy,+dx [+dz] term): positives.
for rows in range(size[0]):
    print(rows)
    for cols in range(size[1]):
        print(cols)
        for items in range(size[0]):
            if items == cols:
                raw_data[rows,cols] = raw_data[rows,cols] + differential*2
                data = np.column_stack((labels,raw_data))
                print(data)
                raw_data[rows,cols] = reset[rows,cols]
            elif items > cols:
                raw_data[rows,cols] = raw_data[rows,cols] + differential
                raw_data[rows,items] = raw_data[rows,items] + differential
                data = np.column_stack((labels,raw_data))
                print(data)
                raw_data[rows,cols] = reset[rows,cols]
                raw_data[rows,items] = reset[rows,items]

# These are the (-x,y),(-x,z),(-y,z) terms.
for rows in range(size[0]):
    print(rows)
    for cols in range(size[1]):
        print(cols)
        for items in range(size[0]):
            if items < cols:
                raw_data[rows,cols] = raw_data[rows,cols] + differential
                raw_data[rows,items] = raw_data[rows,items] - differential
                data = np.column_stack((labels,raw_data))
                print(data)
                raw_data[rows,cols] = reset[rows,cols]
                raw_data[rows,items] = reset[rows,items]
#These are the (x,-y),(x,-z),(y,-z) terms.
            elif items > cols:
                raw_data[rows,cols] = raw_data[rows,cols] + differential
                raw_data[rows,items] = raw_data[rows,items] - differential
                data = np.column_stack((labels,raw_data))
                print(data)
                raw_data[rows,cols] = reset[rows,cols]
                raw_data[rows,items] = reset[rows,items]
        print(cols)
#These are the (-x,-x,): negatives.
for rows in range(size[0]):
    print(rows)
    for cols in range(size[1]):
        print(cols)
        for items in range(size[0]):
            if items == cols:
                raw_data[rows,cols] = raw_data[rows,cols] - differential*2
                data = np.column_stack((labels,raw_data))
                print(data)
                raw_data[rows,cols] = reset[rows,cols]
            elif items > cols:
                raw_data[rows,cols] = raw_data[rows,cols] - differential
                raw_data[rows,items] = raw_data[rows,items] - differential
                data = np.column_stack((labels,raw_data))
                print(data)
                raw_data[rows,cols] = reset[rows,cols]
                raw_data[rows,items] = reset[rows,items]

# To calculate the second derivative, some weird stuff has got to be figured out.