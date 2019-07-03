f = open('reference.out', 'r')
lines = f.readlines()

for line in lines:
    if "CCSD(T)-F12/cc-pVTZ-F12//CCSD(T)-F12/cc-pVTZ-F12 energy" in line:
        line = line.split()
        print(line)
        reference = line[2]

print(reference)
