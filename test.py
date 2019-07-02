f = open('geom.xyz', 'r')
lines = f.readlines()

test = []

for line in lines:
    if "O" in line:
        line = line.split()
        print(line)
        test.append(line[2])

print(test)
