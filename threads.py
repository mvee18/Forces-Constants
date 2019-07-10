import os
import numpy as np
import threading
import subprocess
from threading import Thread
import time

differential = 0.005
nn = 1

reset = np.genfromtxt('geom.xyz', skip_header=1, usecols=(1,2,3))
raw_data = np.genfromtxt('geom.xyz', skip_header=1, usecols=(1,2,3))
labels = np.genfromtxt('geom.xyz', skip_header=1, dtype=str, usecols=0)
memory_list = [50]

# This outputs as (rows,cols):
size = raw_data.shape
num_of_jobs = raw_data.size * 2
input_list = []
for i in range(num_of_jobs):
    input_list.append(i)

# We need the reference energy.
yy = open("reference.out", 'r')
yyy = yy.readlines()
for line in yyy:
    if "CCSD(T)-F12/cc-pVTZ-F12//CCSD(T)-F12/cc-pVTZ-F12 energy" in line:
        line = line.split()
        reference = float(line[2])

def save_and_gen():
    np.savetxt("tmp.txt", data, delimiter=" ", fmt='%s')
    gen_com()

def gen_com(name):
    filename = name
    temp = open(filename, 'r')
    if filename == "tmp.txt":
        f = open("input1.com", 'w+')
    elif filename == "tmp2.txt":
        f = open("input2.com", 'w+')
    elif filename == "tmp3.txt":
        f = open("input3.com", 'w+')
    elif filename == "tmp4.txt":
        f = open("input4.com", 'w+')
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
    subprocess.call("rm tmp*.txt", shell=True)

def gen_pbs(name):
    filename = name
    if filename == "pbs1":
        f = open("input1.pbs", 'w+')
    elif filename == "pbs2":
        f = open("input2.pbs", 'w+')
    elif filename == "pbs3":
        f = open("input3.pbs", 'w+')
    elif filename == "pbs4":
        f = open("input4.pbs", 'w+')
    f.write("#!/bin/sh\n")
    f.write("#PBS -N job{0}\n".format(nn))
    f.write("#PBS -S /bin/bash\n")
    f.write("#PBS -j oe\n")
    f.write("#PBS -W umask=022\n")
    f.write("#PBS -l walltime=00:30:00\n")
    f.write("#PBS -l ncpus=1\n")
    f.write("#PBS -l mem=50mb\n\n")
    f.write("module load intel\n")
    f.write("module load mpt\n")
    f.write("export PATH=/ptmp/bwhopkin/molpro_mpt/2012/molprop_2012_1_Linux_x86_64_i8/bin:$PATH\n\n")

    f.write("export WORKDIR=$PBS_O_WORKDIR\n")
    f.write("export TMPDIR=/tmp/$USER/$PBS_JOBID\n")
    f.write("cd $WORKDIR\n")
    f.write("mkdir -p $TMPDIR\n\n")

    f.write("date\n")
    if filename == "pbs1":
        f.write("mpiexec molpro.exe input1.com\n")
    elif filename == "pbs2":
        f.write("mpiexec molpro.exe input2.com\n")
    elif filename == "pbs3":
        f.write("mpiexec molpro.exe input3.com\n")
    elif filename == "pbs4":
        f.write("mpiexec molpro.exe input4.com\n")
    f.write("date\n\n")

    f.write("rm -rf $TMPDIR")

def sub_job(args):
        subprocess.call("mpiexec molpro.exe input%d.com" %args,shell=True)

threadslist = []

def threads(number):
    thread = Thread(target=sub_job, args=(number,))
    threadslist.append(thread)

def run_jobs():
    print(threadslist)
    for x in threadslist:
        x.start()
        time.sleep(1)
    for x in threadslist:
        x.join()
        time.sleep(1)
    threadslist.clear()

def extract_energy(numberofinput):
    if numberofinput == 1:
        zz = open("input1.out", 'r')
        zzz = zz.readlines()
        for line in zzz:
            if "!CCSD(T)-F12b total energy" in line:
                line = line.split()
                positives.append(line[3])
                zz.close()
    elif numberofinput == 2:
        zz = open("input2.out", 'r')
        zzz = zz.readlines()
        for line in zzz:
            if "!CCSD(T)-F12b total energy" in line:
                line = line.split()
                negatives.append(line[3])
                zz.close()
    elif numberofinput == 3:
        zz = open("input3.out", 'r')
        zzz = zz.readlines()
        for line in zzz:
            if "!CCSD(T)-F12b total energy" in line:
                line = line.split()
                minusplus.append(line[3])
                zz.close()
    elif numberofinput == 4:
        zz = open("input4.out", 'r')
        zzz = zz.readlines()
        for line in zzz:
            if "!CCSD(T)-F12b total energy" in line:
                line = line.split()
                plusminus.append(line[3])
                zz.close()
#    elif posorneg == "doublepositives":
#        sub_job()
#        zz = open("input.out", 'r')
#        zzz = zz.readlines()
#        for line in zzz:
#            if "!CCSD(T)-F12b total energy" in line:
#                line = line.split()
#                doublepositives.append(line[3])
#    elif posorneg == "doublenegatives":
#        sub_job()
#        zz = open("input.out", 'r')
#        zzz = zz.readlines()
#        for line in zzz:
#            if "!CCSD(T)-F12b total energy" in line:
#                line = line.split()
#                doublenegatives.append(line[3])

positives = []
negatives = []
minusplus = []
plusminus = []
doublepositives = []
doublenegatives = []

# First derivatives.
def first_derivative():
    for i in range(len(positives)):
        first_energy = ((float(positives[i]) - float(negatives[i]))/(2*differential))
        positives.clear()
        negatives.clear()
        print(first_energy)
        #if i % 3 == 0:
        #    print("d/dx:")
        #    print(first_energy)
        #elif i % 3 == 1:
        #    print("d/dy:")
        #    print(first_energy)
        #elif i % 3 == 2:
        #    print("d/dz")
        #    print(first_energy)

# Second Derivatives for double displacements.
def second_derivative_a():
    for i in range(len(e)):
        second_energy = (e[i] - 2*reference + f[i]) / ((differential*2)**2)
        print(second_energy)

# More complicated second derivatives:
def second_derivative_b():
    for i in range(len(a)):
        second_energy_b = (a[i] - b[i] - c[i] + d[i])/(4*(differential**2))
        print(second_energy_b)

# FIRST DISP GENERATION
for rows in range(size[0]):
    for cols in range(size[1]):
        raw_data[rows,cols] = raw_data[rows,cols] + differential
        pos_dif = np.column_stack((labels,raw_data))
        np.savetxt("tmp.txt", pos_dif, delimiter=" ", fmt='%s')
        print(pos_dif)
        gen_com("tmp.txt")
        gen_pbs("pbs1")
        threads(1)
        nn += 1
        raw_data[rows,cols] = reset[rows,cols]

        raw_data[rows,cols] = raw_data[rows,cols] - differential
        neg_dif = np.column_stack((labels,raw_data))
        np.savetxt("tmp2.txt", neg_dif, delimiter=" ", fmt='%s')
        print(neg_dif)
        gen_com("tmp2.txt")
        gen_pbs("pbs2")
        threads(2)
        nn += 1
        run_jobs()
# you can clean this up by combining the arguments.
        extract_energy(1)
        extract_energy(2)
        first_derivative()
        subprocess.call("rm input*.com*", shell=True)
        subprocess.call("rm input*.pbs*", shell=True)
        raw_data[rows,cols] = reset[rows,cols]

print(threadslist)

"""
for i in range(size[0]):
    for cols in range(size[1]):
        raw_data[rows,cols] = raw_data[rows,cols] - differential
        neg_dif = np.column_stack((labels,raw_data))
        np.savetxt("tmp.txt", neg_dif, delimiter=" ", fmt='%s')
#        gen_com()
#        extract_energy("negatives")
        raw_data[rows,cols] = reset[rows,cols]


# first_derivative()
"""

print(positives)
print(negatives)

positives.clear()
negatives.clear()

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
e = doublepositives
f = doublenegatives

# This is for all ways to add two terms together.


for rows in range(size[0]):
    print(rows)
    for cols in range(size[1]):
        print(cols)
        for items in range(size[1]):
            if items == cols:
# This is the +[xx,yy,zz] term.
                raw_data[rows,cols] = raw_data[rows,cols] + differential*2
                data = np.column_stack((labels,raw_data))
                # save_and_gen()
                # extract_energy("doublepositives")
                print(data)
                raw_data[rows,cols] = reset[rows,cols]
# This is the -[xx,yy,zz] term.
                raw_data[rows,cols] = raw_data[rows,cols] - differential*2
                data = np.column_stack((labels,raw_data))
                # save_and_gen()
                # extract_energy("doublenegatives")
                print(data)
                raw_data[rows,cols] = reset[rows,cols]

            elif items > cols:
# These are the ways to arrange two terms together: positives.
                raw_data[rows,cols] = raw_data[rows,cols] + differential
                raw_data[rows,items] = raw_data[rows,items] + differential
                data = np.column_stack((labels,raw_data))
                # save_and_gen()
                # extract_energy("positives")
                print(data)
                raw_data[rows,cols] = reset[rows,cols]
                raw_data[rows,items] = reset[rows,items]
# These are the ways to arrange the -,-: negatives.
                raw_data[rows,cols] = raw_data[rows,cols] - differential
                raw_data[rows,items] = raw_data[rows,items] - differential
                data = np.column_stack((labels,raw_data))
                #save_and_gen()
                #extract_energy("negatives")
                print(data)
                raw_data[rows,cols] = reset[rows,cols]
                raw_data[rows,items] = reset[rows,items]
# -,+: minusplus
                raw_data[rows,cols] = raw_data[rows,cols] - differential
                raw_data[rows,items] = raw_data[rows,items] + differential
                data = np.column_stack((labels,raw_data))
                #save_and_gen()
                #extract_energy("minusplus")
                print(data)
                raw_data[rows,cols] = reset[rows,cols]
                raw_data[rows,items] = reset[rows,items]
#+,-: plusminus
                raw_data[rows,cols] = raw_data[rows,cols] + differential
                raw_data[rows,items] = raw_data[rows,items] - differential
                data = np.column_stack((labels,raw_data))
                #save_and_gen()
                #extract_energy("plusminus")
                print(data)
                raw_data[rows,cols] = reset[rows,cols]
                raw_data[rows,items] = reset[rows,items]
#Vertical distribution of displacements.
        for i in range(size[0]):
            if i == rows:
# X1 term.
                raw_data[rows,cols] = raw_data[rows,cols] + differential *2
                data = np.column_stack((labels,raw_data))
                print(data)
                raw_data[rows,cols] = reset[rows,cols]
                raw_data[i,cols] = reset[i,cols]
# -X1 term.
                raw_data[rows,cols] = raw_data[rows,cols] - differential * 2
                data = np.column_stack((labels,raw_data))
                print(data)
                raw_data[rows,cols] = reset[rows,cols]
                raw_data[i,cols] = reset[i,cols]

            elif i > rows:
# X1 and X2...
                print(i)
                raw_data[rows,cols] = raw_data[rows,cols] + differential
                raw_data[i,cols] = raw_data[i,cols] + differential
                data = np.column_stack((labels,raw_data))
                print(data)
                raw_data[rows,cols] = reset[rows,cols]
                raw_data[i,cols] = reset[i,cols]
#-X1 and -X2
                raw_data[rows,cols] = raw_data[rows,cols] - differential
                raw_data[i,cols] = raw_data[i,cols] - differential
                data = np.column_stack((labels,raw_data))
                print(data)
                raw_data[rows,cols] = reset[rows,cols]
                raw_data[i,cols] = reset[i,cols]
# -X1 and X2
                raw_data[rows,cols] = raw_data[rows,cols] - differential
                raw_data[i,cols] = raw_data[i,cols] + differential
                data = np.column_stack((labels,raw_data))
                print(data)
                raw_data[rows,cols] = reset[rows,cols]
                raw_data[i,cols] = reset[i,cols]
# X1 and -X2.
                raw_data[rows,cols] = raw_data[rows,cols] + differential
                raw_data[i,cols] = raw_data[i,cols] - differential
                data = np.column_stack((labels,raw_data))
                print(data)
                raw_data[rows,cols] = reset[rows,cols]
                raw_data[i,cols] = reset[i,cols]


"""
# These are the (-x,y),(-x,z),(-y,z) terms.
for rows in range(size[0]):
    print(rows)
    for cols in range(size[1]):
        print(cols)
        for items in range(size[0]):
            if items > cols:
                raw_data[rows,cols] = raw_data[rows,cols] - differential
                raw_data[rows,items] = raw_data[rows,items] + differential
                data = np.column_stack((labels,raw_data))
                save_and_gen()
                extract_energy("minusplus")
                print(data)
                raw_data[rows,cols] = reset[rows,cols]
                raw_data[rows,items] = reset[rows,items]
        for i in range(size[0]):
            if i > rows:
                print(i)
                raw_data[rows,cols] = raw_data[rows,cols] - differential
                raw_data[i,cols] = raw_data[i,cols] + differential
                data = np.column_stack((labels,raw_data))
                print(data)
                raw_data[rows,cols] = reset[rows,cols]
                raw_data[i,cols] = reset[i,cols]

#These are the (x,-y),(x,-z),(y,-z) terms.
for rows in range(size[0]):
    print(rows)
    for cols in range(size[1]):
        print(cols)
        for items in range(size[0]):
            if items > cols:
                raw_data[rows,cols] = raw_data[rows,cols] + differential
                raw_data[rows,items] = raw_data[rows,items] - differential
                data = np.column_stack((labels,raw_data))
                save_and_gen()
                extract_energy("plusminus")
                print(data)
                raw_data[rows,cols] = reset[rows,cols]
                raw_data[rows,items] = reset[rows,items]
        for i in range(size[0]):
            if i > rows:
                print(i)
                raw_data[rows,cols] = raw_data[rows,cols] + differential
                raw_data[i,cols] = raw_data[i,cols] - differential
                data = np.column_stack((labels,raw_data))
                print(data)
                raw_data[rows,cols] = reset[rows,cols]
                raw_data[i,cols] = reset[i,cols]

#These are the (-x,-x,): negatives.
for rows in range(size[0]):
    print(rows)
    for cols in range(size[1]):
        print(cols)
        for items in range(size[0]):
            if items == cols:
                raw_data[rows,cols] = raw_data[rows,cols] - differential*2
                data = np.column_stack((labels,raw_data))
                save_and_gen()
                extract_energy("doublenegatives")
                print(data)
                raw_data[rows,cols] = reset[rows,cols]
            elif items > cols:
                raw_data[rows,cols] = raw_data[rows,cols] - differential
                raw_data[rows,items] = raw_data[rows,items] - differential
                data = np.column_stack((labels,raw_data))
                save_and_gen()
                extract_energy("negatives")
                print(data)
                raw_data[rows,cols] = reset[rows,cols]
                raw_data[rows,items] = reset[rows,items]
        for i in range(size[0]):
            if i > rows:
                print(i)
                raw_data[rows,cols] = raw_data[rows,cols] - differential
                raw_data[i,cols] = raw_data[i,cols] - differential
                data = np.column_stack((labels,raw_data))
                print(data)
                raw_data[rows,cols] = reset[rows,cols]
                raw_data[i,cols] = reset[i,cols]

# To calculate the second derivative, some weird stuff has got to be figured out.
a = [float(i) for i in a]
b = [float(i) for i in b]
c = [float(i) for i in c]
d = [float(i) for i in d]
e = [float(i) for i in e]
f = [float(i) for i in f]
reference = float(reference)

second_derivative_a()
second_derivative_b()
"""
print(a)
print(b)
print(c)
print(d)
print(e)
print(f)

import psutil
process = psutil.Process(os.getpid())
print(process.memory_info()[0])
