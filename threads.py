import os
import numpy as np
import threading
import subprocess
from threading import Thread
import time

import psutil
process = psutil.Process(os.getpid())

differential = 0.005
global nn
nn = 1

reset = np.genfromtxt('geom.xyz', skip_header=1, usecols=(1,2,3))
raw_data = np.genfromtxt('geom.xyz', skip_header=1, usecols=(1,2,3))
labels = np.genfromtxt('geom.xyz', skip_header=1, dtype=str, usecols=0)
memory_list = [50]

# This outputs as (rows,cols):
size = raw_data.shape
num_of_jobs = raw_data.size

print(size[0])

# We need the reference energy.
yy = open("reference.out", 'r')
yyy = yy.readlines()
for line in yyy:
    if "!CCSD(T)-F12b total energy" in line:
        line = line.split()
        reference = float(line[3])
"""
def save_and_gen(args):
    np.savetxt("tmp.txt", data, delimiter=" ", fmt='%s')
    gen_com()
"""

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
    elif filename == "tmp5.txt":
        f = open("input5.com", 'w+')
    elif filename == "tmp6.txt":
        f = open("input6.com", 'w+')
    elif filename == "tmp7.txt":
        f = open("input7.com", 'w+')
    elif filename == "tmp8.txt":
        f = open("input8.com", 'w+')
    f.write("memory,%d,m\n" %memory_list[0])
    f.write("gthresh,energy=1.d-12,zero=1.d-22,oneint=1.d-22,twoint=1.d-22;\n")
#            gthresh,optgrad=1.d-8,optstep=1.d-8;
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
    f.write("{hf;accu,20;}\n")
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
    elif filename == "pbs5":
        f = open("input5.pbs", 'w+')
    elif filename == "pbs6":
        f = open("input6.pbs", 'w+')
    elif filename == "pbs7":
        f = open("input7.pbs", 'w+')
    elif filename == "pbs8":
        f = open("input8.pbs", 'w+')
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
    elif filename == "pbs5":
        f.write("mpiexec molpro.exe input5.com\n")
    elif filename == "pbs6":
        f.write("mpiexec molpro.exe input6.com\n")
    elif filename == "pbs7":
        f.write("mpiexec molpro.exe input7.com\n")
    elif filename == "pbs8":
        f.write("mpiexec molpro.exe input8.com\n")
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
#                Found = True
                line = line.split()
                negatives.append(line[3])
                zz.close()
#                if Found = False:
#                    print(nn)
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
    elif numberofinput == 5:
        zz = open("input5.out", 'r')
        zzz = zz.readlines()
        for line in zzz:
            if "!CCSD(T)-F12b total energy" in line:
                line = line.split()
                doublepositives.append(line[3])
                zz.close()
    elif numberofinput == 6:
        zz = open("input6.out", 'r')
        zzz = zz.readlines()
        for line in zzz:
            if "!CCSD(T)-F12b total energy" in line:
                line = line.split()
                doublenegatives.append(line[3])
                zz.close()
    elif numberofinput == 7:
        zz = open("input7.out", 'r')
        zzz = zz.readlines()
        for line in zzz:
            if "!CCSD(T)-F12b total energy" in line:
                line = line.split()
                seven_list.append(line[3])
                zz.close()
    elif numberofinput == 8:
        zz = open("input8.out", 'r')
        zzz = zz.readlines()
        for line in zzz:
            if "!CCSD(T)-F12b total energy" in line:
                line = line.split()
                eight_list.append(line[3])
                zz.close()

positives = []
negatives = []
minusplus = []
plusminus = []
doublepositives = []
doublenegatives = []
seven_list = []
eight_list = []

# First derivatives.
# Could speed this up by removing the iterator, since there is no longer more than one item in the list.
def first_derivative():
    for i in range(len(positives)):
        first_energy = ((float(positives[i]) - float(negatives[i]))/(2*differential))
        positives.clear()
        negatives.clear()

second_energy_list_a = []
second_energy_list_b = []

# Second Derivatives for double displacements.
# Could speed this up by removing the iterator, since there is no longer more than one item in the list.
def second_derivative_a():
    for i in range(len(e)):
        second_energy = (float(e[i]) - 2*reference + float(f[i])) / ((differential*2)**2)
        e.clear()
        f.clear()
        print(second_energy)
        second_energy_list_a.append(second_energy)
        return second_energy

# More complicated second derivatives:
def second_derivative_b():
    for i in range(len(a)):
        second_energy_b = (float(a[i]) - float(b[i]) - float(c[i]) + float(d[i]))/(4*(differential**2))
        a.clear()
        b.clear()
        c.clear()
        d.clear()
        print(second_energy_b)
        second_energy_list_b.append(second_energy_b)
        return second_energy_b

"""
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
        subprocess.call("rm input*.out*", shell=True)
        subprocess.call("rm input*.xml*", shell=True)
        raw_data[rows,cols] = reset[rows,cols]
"""

positives.clear()
negatives.clear()

# Second derivatives.

# Redefine lists to help me understand.
a = positives
b = plusminus
c = minusplus
d = negatives
e = doublepositives
ff = doublenegatives
g = seven_list
h = eight_list

# This is for all ways to add two terms together.

zero_array = np.zeros((27,3))

zero_size = zero_array.shape

item_count = 0
doubles = 0
x_list = 0

print(zero_size)

"""
#Array generation: these will be edited later to work for larger arrays.
array = []
for atom1 in range(size[0]):
    coordinate_list1 = []
    for coordinate1 in range(size[0]):
        atom_list1 = []
        for atom2 in range(size[0]):
            coordinate_list2 = []
            for coordinate2 in range(size[0]):
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
    print(a1,c1,a2,c2)
    if a1 == a2 and c1 == c2:
        nn = 0
        raw_data[a1,c1] = raw_data[a1,c1] + differential*2
        pos_dif = np.column_stack((labels,raw_data))
        print(pos_dif)
        np.savetxt("tmp5.txt", pos_dif, delimiter=" ", fmt='%s')
        gen_com("tmp5.txt")
        gen_pbs("pbs5")
        threads(5)
        nn+=1
        raw_data[a1,c1] = reset[a1,c1]

        raw_data[a2,c2] = raw_data[a2,c2] - differential*2
        neg_dif = np.column_stack((labels,raw_data))
        print(neg_dif)
        np.savetxt("tmp6.txt", neg_dif, delimiter=" ", fmt='%s')
        gen_com("tmp6.txt")
        gen_pbs("pbs6")
        threads(6)
        nn+=1
        raw_data[a2,c2] = reset[a2,c2]

        run_jobs()
        extract_energy(5)
        extract_energy(6)
        energy = second_derivative_a()
        print(energy)

        energy = (energy * (0.529177208)**2)
        array[a1,c1,a2,c2] = energy
        array[a2,c2,a1,c1] = energy

        subprocess.call("rm input*.com*", shell=True)
        subprocess.call("rm input*.out*", shell=True)
        subprocess.call("rm input*.pbs*", shell=True)
        subprocess.call("rm input*.xml*", shell=True)
        raw_data[a1,c1] = reset[a1,c1]
    else:
        nn = 0
        raw_data[a1,c1] = raw_data[a1,c1] + differential
        raw_data[a2,c2] = raw_data[a2,c2] + differential
        data = np.column_stack((labels,raw_data))
        np.savetxt("tmp.txt", data, delimiter=" ", fmt='%s')
        print(data)
        gen_com("tmp.txt")
        gen_pbs("pbs1")
        threads(1)
        nn+=1
        raw_data[a1,c1] = reset[a1,c1]
        raw_data[a2,c2] = reset[a2,c2]

        raw_data[a1,c1] = raw_data[a1,c1] - differential
        raw_data[a2,c2] = raw_data[a2,c2] - differential
        data = np.column_stack((labels,raw_data))
        np.savetxt("tmp2.txt", data, delimiter=" ", fmt='%s')
        print(data)
        gen_com("tmp2.txt")
        gen_pbs("pbs2")
        threads(2)
        nn+=1
        raw_data[a1,c1] = reset[a1,c1]
        raw_data[a2,c2] = reset[a2,c2]

        raw_data[a1,c1] = raw_data[a1,c1] - differential
        raw_data[a2,c2] = raw_data[a2,c2] + differential
        data = np.column_stack((labels,raw_data))
        np.savetxt("tmp3.txt", data, delimiter=" ", fmt='%s')
        print(data)
        gen_com("tmp3.txt")
        gen_pbs("pbs3")
        threads(3)
        nn+=1
        raw_data[a1,c1] = reset[a1,c1]
        raw_data[a2,c2] = reset[a2,c2]

        raw_data[a1,c1] = raw_data[a1,c1] + differential
        raw_data[a2,c2] = raw_data[a2,c2] - differential
        data = np.column_stack((labels,raw_data))
        np.savetxt("tmp4.txt", data, delimiter=" ", fmt='%s')
        print(data)
        gen_com("tmp4.txt")
        gen_pbs("pbs4")
        threads(4)
        nn+=1

        run_jobs()
        extract_energy(1)
        extract_energy(2)
        extract_energy(3)
        extract_energy(4)
        energyb = second_derivative_b()
        energyb = (energyb*(0.529177208)**2)
        print(energyb)
        array[a1,c1,a2,c2] = energyb
        array[a2,c2,a1,c1] = energyb

        subprocess.call("rm input*.com*", shell=True)
        subprocess.call("rm input*.out*", shell=True)
        subprocess.call("rm input*.pbs*", shell=True)
        subprocess.call("rm input*.xml*", shell=True)
        raw_data[a1,c1] = reset[a1,c1]
        raw_data[a2,c2] = reset[a2,c2]
#XYZ Flagging

array = array.astype(float)
print(array.dtype)

for i in range(shapefour[0]):
    for j in range(shapefour[1]):
        Found = False
        for k in range(shapefour[2]):
            for l in range(shapefour[3]):
                if i == k and j == l:
#                    array[i,j,k,l] = o[element1]
#                    array[k,l,i,j] = o[element1]
                    value = (i,j,k,l)
                    res = convert(value)
                    Found = True
                    print(i,j,k,l)
#                    element1 +=
                    manipulate_geometry_second(i,j,k,l)
                elif Found:
                    comparison_list = (i,j,k,l)
                    comparevalue = convert(comparison_list)
                    if comparevalue > res:
#                        array[i,j,k,l] = p[element2]
#                        array[k,l,i,j] = p[element2]
                        print(comparevalue, res)
                        print(i,j,k,l)
                        manipulate_geometry_second(i,j,k,l)
#                        element2 += 1

np.set_printoptions(suppress=True,
   formatter={'float_kind':'{:20.10f}'.format})

final = []

for i in range(shapefour[0]):
    for j in range(shapefour[1]):
        for k in range(shapefour[2]):
            final.append(array[i,j,k].tolist())

final = np.asarray(final)
print(final)

e = open('fort.15','w+')
#Generalize this.
e.write('    3   18')
np.savetxt('fort.15',final,fmt='%20.10f')

a = positives
b = plusminus
c = minusplus
d = negatives
e = doublepositives
ff = doublenegatives
g = seven_list
h = eight_list

third_list = []

def determine_atom(row,atom_number,item):
    if int(third_array[row, atom_number, item]) // 3 == 0:
        third_array[row,atom_number,item] = 0
    elif int(third_array[row, atom_number,item]) // 3 == 1:
        third_array[row,atom_number,item] = 1
    elif int(third_array[row,atom_number,item]) // 3 == 2:
        third_array[row,atom_number,item] = 2

def determine_coordinate(row,coordinate_number,item):
    if int(third_array[row, coordinate_number,item]) % 3 == 0:
        third_array[row,coordinate_number,item] = 0
    elif int(third_array[row, coordinate_number,item]) % 3 == 1:
        third_array[row,coordinate_number,item] = 1
    elif int(third_array[row,coordinate_number,item]) % 3 == 2:
        third_array[row,coordinate_number,item] = 2

def double_third_terms(zipped,paired,unpaired):
    print(paired,unpaired)
    raw_data[zipped[paired]] = raw_data[zipped[paired]] + 2 * differential
    raw_data[zipped[unpaired]] = raw_data[zipped[unpaired]] + differential
#    print(raw_data)
    data = np.column_stack((labels,raw_data))
    np.savetxt("tmp.txt", data, delimiter=" ", fmt='%s')
    print(data)
    gen_com("tmp.txt")
    gen_pbs("pbs1")
    threads(1)
    raw_data[:] = reset[:]

    raw_data[zipped[unpaired]] = raw_data[zipped[unpaired]] + differential
#    print(raw_data)
    data = np.column_stack((labels,raw_data))
    np.savetxt("tmp2.txt", data, delimiter=" ", fmt='%s')
    print(data)
    gen_com("tmp2.txt")
    gen_pbs("pbs2")
    threads(2)
    raw_data[:] = reset[:]

    raw_data[zipped[paired]] = raw_data[zipped[paired]] - 2 * differential
    raw_data[zipped[unpaired]] = raw_data[zipped[unpaired]] + differential
#    print(raw_data)
    data = np.column_stack((labels,raw_data))
    np.savetxt("tmp3.txt", data, delimiter=" ", fmt='%s')
    print(data)
    gen_com("tmp3.txt")
    gen_pbs("pbs3")
    threads(3)
    raw_data[:] = reset[:]

    raw_data[zipped[paired]] = raw_data[zipped[paired]] + 2 * differential
    raw_data[zipped[unpaired]] = raw_data[zipped[unpaired]] - differential
#    print(raw_data)
    data = np.column_stack((labels,raw_data))
    np.savetxt("tmp4.txt", data, delimiter=" ", fmt='%s')
    print(data)
    gen_com("tmp4.txt")
    gen_pbs("pbs4")
    threads(4)
    raw_data[:] = reset[:]

    raw_data[zipped[unpaired]] = raw_data[zipped[unpaired]] - differential
#    print(raw_data)
    data = np.column_stack((labels,raw_data))
    np.savetxt("tmp5.txt", data, delimiter=" ", fmt='%s')
    print(data)
    gen_com("tmp5.txt")
    gen_pbs("pbs5")
    threads(5)
    raw_data[:] = reset[:]

    raw_data[zipped[paired]] = raw_data[zipped[paired]] - 2 * differential
    raw_data[zipped[unpaired]] = raw_data[zipped[unpaired]] - differential
#    print(raw_data)
    data = np.column_stack((labels,raw_data))
    np.savetxt("tmp6.txt", data, delimiter=" ", fmt='%s')
    print(data)
    gen_com("tmp6.txt")
    gen_pbs("pbs6")
    threads(6)
    raw_data[:] = reset[:]

    run_jobs()
    extract_energy(1)
    extract_energy(2)
    extract_energy(3)
    extract_energy(4)
    extract_energy(5)
    extract_energy(6)
    third_derivatives_b()
    subprocess.call("rm input*.com*", shell=True)
    subprocess.call("rm input*.out*", shell=True)
    subprocess.call("rm input*.pbs*", shell=True)
    subprocess.call("rm input*.xml*", shell=True)


# Note that coord1 = z, coord2 = y, coord3 = x.
def triple_third_terms(coord1,coord2,coord3,zipped):
    raw_data[zipped[coord1]] = raw_data[zipped[coord1]] + differential
    raw_data[zipped[coord2]] = raw_data[zipped[coord2]] + differential
    raw_data[zipped[coord3]] = raw_data[zipped[coord3]] + differential
#    print(raw_data)
    data = np.column_stack((labels,raw_data))
    np.savetxt("tmp.txt", data, delimiter=" ", fmt='%s')
    print(data)
    gen_com("tmp.txt")
    gen_pbs("pbs1")
    threads(1)
    raw_data[:] = reset[:]

    raw_data[zipped[coord1]] = raw_data[zipped[coord1]] + differential
    raw_data[zipped[coord2]] = raw_data[zipped[coord2]] - differential
    raw_data[zipped[coord3]] = raw_data[zipped[coord3]] + differential
#    print(raw_data)
    data = np.column_stack((labels,raw_data))
    np.savetxt("tmp2.txt", data, delimiter=" ", fmt='%s')
    print(data)
    gen_com("tmp2.txt")
    gen_pbs("pbs2")
    threads(2)
    raw_data[:] = reset[:]

    raw_data[zipped[coord1]] = raw_data[zipped[coord1]] + differential
    raw_data[zipped[coord2]] = raw_data[zipped[coord2]] + differential
    raw_data[zipped[coord3]] = raw_data[zipped[coord3]] - differential
#    print(raw_data)
    data = np.column_stack((labels,raw_data))
    np.savetxt("tmp3.txt", data, delimiter=" ", fmt='%s')
    print(data)
    gen_com("tmp3.txt")
    gen_pbs("pbs3")
    threads(3)
    raw_data[:] = reset[:]

    raw_data[zipped[coord1]] = raw_data[zipped[coord1]] + differential
    raw_data[zipped[coord2]] = raw_data[zipped[coord2]] - differential
    raw_data[zipped[coord3]] = raw_data[zipped[coord3]] - differential
#    print(raw_data)
    data = np.column_stack((labels,raw_data))
    np.savetxt("tmp4.txt", data, delimiter=" ", fmt='%s')
    print(data)
    gen_com("tmp4.txt")
    gen_pbs("pbs4")
    threads(4)
    raw_data[:] = reset[:]

    raw_data[zipped[coord1]] = raw_data[zipped[coord1]] - differential
    raw_data[zipped[coord2]] = raw_data[zipped[coord2]] + differential
    raw_data[zipped[coord3]] = raw_data[zipped[coord3]] + differential
#    print(raw_data)
    data = np.column_stack((labels,raw_data))
    np.savetxt("tmp5.txt", data, delimiter=" ", fmt='%s')
    print(data)
    gen_com("tmp5.txt")
    gen_pbs("pbs5")
    threads(5)
    raw_data[:] = reset[:]

    raw_data[zipped[coord1]] = raw_data[zipped[coord1]] - differential
    raw_data[zipped[coord2]] = raw_data[zipped[coord2]] - differential
    raw_data[zipped[coord3]] = raw_data[zipped[coord3]] + differential
#    print(raw_data)
    data = np.column_stack((labels,raw_data))
    np.savetxt("tmp6.txt", data, delimiter=" ", fmt='%s')
    print(data)
    gen_com("tmp6.txt")
    gen_pbs("pbs6")
    threads(6)
    raw_data[:] = reset[:]

    raw_data[zipped[coord1]] = raw_data[zipped[coord1]] - differential
    raw_data[zipped[coord2]] = raw_data[zipped[coord2]] + differential
    raw_data[zipped[coord3]] = raw_data[zipped[coord3]] - differential
#    print(raw_data)
    data = np.column_stack((labels,raw_data))
    np.savetxt("tmp7.txt", data, delimiter=" ", fmt='%s')
    print(data)
    gen_com("tmp7.txt")
    gen_pbs("pbs7")
    threads(7)
    raw_data[:] = reset[:]

    raw_data[zipped[coord1]] = raw_data[zipped[coord1]] - differential
    raw_data[zipped[coord2]] = raw_data[zipped[coord2]] - differential
    raw_data[zipped[coord3]] = raw_data[zipped[coord3]] - differential
#    print(raw_data)
    data = np.column_stack((labels,raw_data))
    np.savetxt("tmp8.txt", data, delimiter=" ", fmt='%s')
    print(data)
    gen_com("tmp8.txt")
    gen_pbs("pbs8")
    threads(8)
    raw_data[:] = reset[:]

    run_jobs()
    extract_energy(1)
    extract_energy(2)
    extract_energy(3)
    extract_energy(4)
    extract_energy(5)
    extract_energy(6)
    extract_energy(7)
    extract_energy(8)
    third_derivatives_c()
    subprocess.call("rm input*.com*", shell=True)
    subprocess.call("rm input*.out*", shell=True)
    subprocess.call("rm input*.pbs*", shell=True)
    subprocess.call("rm input*.xml*", shell=True)
#THIRD DERIVATIVES.
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

#print(third_array)

row_list = []
col_list = []

third_energy_array = []

a = positives
b = negatives
c = minusplus
d = plusminus
e = doublepositives
ff = doublenegatives
g = seven_list
h = eight_list

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
            data = np.column_stack((labels,raw_data))
            np.savetxt("tmp.txt", data, delimiter=" ", fmt='%s')
            print(data)
            gen_com("tmp.txt")
            gen_pbs("pbs1")
            threads(1)
            raw_data[:] = reset[:]

            raw_data[zipped[0]] = raw_data[zipped[0]] - 3*differential
            data = np.column_stack((labels,raw_data))
            np.savetxt("tmp2.txt", data, delimiter=" ", fmt='%s')
            print(data)
            gen_com("tmp2.txt")
            gen_pbs("pbs2")
            threads(2)
            raw_data[:] = reset[:]

            raw_data[zipped[0]] = raw_data[zipped[0]] + differential
            data = np.column_stack((labels,raw_data))
            np.savetxt("tmp3.txt", data, delimiter=" ", fmt='%s')
            print(data)
            gen_com("tmp3.txt")
            gen_pbs("pbs3")
            threads(3)
            raw_data[:] = reset[:]

            raw_data[zipped[0]] = raw_data[zipped[0]] - differential
            data = np.column_stack((labels,raw_data))
            np.savetxt("tmp4.txt", data, delimiter=" ", fmt='%s')
            print(data)
            gen_com("tmp4.txt")
            gen_pbs("pbs4")
            threads(4)
            raw_data[:] = reset[:]

            run_jobs()
            extract_energy(1)
            extract_energy(2)
            extract_energy(3)
            extract_energy(4)
            third_derivatives_a()
            subprocess.call("rm input*.com*", shell=True)
            subprocess.call("rm input*.out*", shell=True)
            subprocess.call("rm input*.pbs*", shell=True)
            subprocess.call("rm input*.xml*", shell=True)

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
            triple_third_terms(0,1,2,zipped)

        else:
            raise Exception("Unable to iterate over all coordinates. Check the geometry.")
        row_list.clear()
        col_list.clear()

def third_derivatives_a():
    print(a,c,d,b)
    third_energy_a = ((float(a[0])
                    - 3*float(c[0])
                    + 3*float(d[0])
                    - float(b[0])))

    third_energy_a = third_energy_a * ((2*differential)**3)
    third_energy_a = (third_energy_a * (0.529177208)**3)
    print(third_energy_a)
    third_energy_array.append(third_energy_a)
    a.clear()
    b.clear()
    c.clear()
    d.clear()

def third_derivatives_b():
    print(a,b,c,d,e,ff)
    third_energy_b = ((float(a[0])
                    - 2*float(b[0])
                    + float(c[0])
                    - float(d[0])
                    + 2*float(e[0])
                    - float(ff[0])))

    third_energy_b = third_energy_b / ((differential*2)**2)
    third_energy_b = third_energy_b / (differential*2)
    third_energy_b = (third_energy_b * (0.529177208)**3)
    print(third_energy_b)
    third_energy_array.append(third_energy_b)
    a.clear()
    b.clear()
    c.clear()
    d.clear()
    e.clear()
    ff.clear()

def third_derivatives_c():
    print(a,b,c,d,e,ff,g,h)
    third_energy_c = ((float(a[0])
                    - float(b[0])
                    - float(c[0])
                    + float(d[0])
                    - float(e[0])
                    + float(ff[0])
                    + float(g[0])
                    - float(h[0])))

    third_energy_c = third_energy_c / (4*(differential**2))
    third_energy_c = third_energy_c * (1/(2*differential))
    third_energy_c = (third_energy_c * (0.529177208)**3)
    third_energy_array.append(third_energy_c)
    print(third_energy_c)
    a.clear()
    b.clear()
    c.clear()
    d.clear()
    e.clear()
    ff.clear()
    g.clear()
    h.clear()

third_geometries()

def determinethirdsize(size):
    total_points_tally = []

    size_of_data = size
    for i in range(1,size_of_data+1,1):
        for j in range(i):
            total_points_tally.append(j+1)

    total_points = int(sum(total_points_tally))
    return total_points//3

print(third_energy_array)

np.set_printoptions(suppress=True,
   formatter={'float_kind':'{:20.10f}'.format})

array = np.reshape(third_energy_array,(determinethirdsize(num_of_jobs),3))
print(array)

e = open('fort.30','w+')

#Generalize this.
np.savetxt('fort.30',array,header='    3   165',fmt='%20.10f',comments='')
"""

# Fourth Derivatives.

fourth_list = []

def determine_atom(row,atom_number,item):
    if int(fourth_array[row, atom_number, item]) // 3 == 0:
        fourth_array[row,atom_number,item] = 0
    elif int(fourth_array[row, atom_number,item]) // 3 == 1:
        fourth_array[row,atom_number,item] = 1
    elif int(fourth_array[row,atom_number,item]) // 3 == 2:
        fourth_array[row,atom_number,item] = 2

def determine_coordinate(row,coordinate_number,item):
    if int(fourth_array[row, coordinate_number,item]) % 3 == 0:
        fourth_array[row,coordinate_number,item] = 0
    elif int(fourth_array[row, coordinate_number,item]) % 3 == 1:
        fourth_array[row,coordinate_number,item] = 1
    elif int(fourth_array[row,coordinate_number,item]) % 3 == 2:
        fourth_array[row,coordinate_number,item] = 2

for w in range(num_of_jobs):
    for x in range(num_of_jobs):
        for y in range(num_of_jobs):
            for z in range(num_of_jobs):
                if x <= w and y <= x and z <= y:
                    fourth_list.append(((w,w),(x,x),(y,y),(z,z)))

fourth_array = np.asarray(fourth_list)

fourth_array_shape = fourth_array.shape
print(fourth_array_shape)

for row in range(fourth_array_shape[0]):
    for col in range(fourth_array_shape[1]):
        pair = 0
        if pair == 0:
            determine_atom(row,col,pair)
    for col in range(fourth_array_shape[1]):
        pair = 1
        if pair == 1:
            fourth_array[row,col,1] = int(fourth_array[row,col,1])
            determine_coordinate(row,col,1)

print(fourth_array)

fourth_row_list = []
fourth_col_list = []

def fourth_geometries():
    for i in range(fourth_array_shape[0]):
        for j in range(fourth_array_shape[1]):
            fourth_row_list.append(fourth_array[i,j,0])
            fourth_col_list.append(fourth_array[i,j,1])
        zipped = zip(fourth_row_list,fourth_col_list)
        zipped = list(zipped)
        print(zipped)
        fourth_row_list.clear()
        fourth_col_list.clear()

fourth_geometries()
print(process.memory_info()[0])
