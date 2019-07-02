import os
import numpy as np

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

def header(differentialtype):
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
        f.close()
        temp.close()

# First derivatives.

def first_deriative(epos,eneg):
    first_energy = (float(epos) - float(eneg)/(2*differential))
    print(first_energy)
    return

#After header, we will have to do the submission.
for rows in range(size[0]):
    for cols in range(size[1]):
        raw_data[rows,cols] = raw_data[rows,cols] + differential
        pos_dif = np.column_stack((labels,raw_data))
        np.savetxt("tmp.txt", pos_dif, delimiter=" ", fmt='%s')
        header(pos_dif)
        raw_data[rows,cols] = reset[rows,cols]

for i in range(size[0]):
    for cols in range(size[1]):
        raw_data[rows,cols] = raw_data[rows,cols] - differential
        neg_dif = np.column_stack((labels,raw_data))
        np.savetxt("tmp.txt", neg_dif, delimiter=" ", fmt='%s')
        header(neg_dif)
        raw_data[rows,cols] = reset[rows,cols]

# Second derivatives.
# We need the following pairs: [(x1,xn),(y1,yn),(z1.zn),(x1,yn),(x1,zn),(y1,zn)], without repeating.

# I used a triple loop in order to assign a third dimension to the array, which is the item number within the line.
# This keeps track of xyz that the currently [row,col] value needs to be added to.
# If the item # = the col, then they are the same, and the dif needs to be added twice.
# If the item # > col, then it needs to add the two. Iterating this is equivalent to creating the permuations.
# Most significantly, this prevents double counting.


# This is for all ways to add two terms together (+dy,+dx [+dz] term)
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

#These are the (-x,-x,)
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
