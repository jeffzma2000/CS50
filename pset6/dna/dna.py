import sys
import csv

# checks the number of arguments is correct
if len(sys.argv) != 3:
    sys.exit("Usage: python dna.py infile outfile")

# reads the file into a dictionary
file = csv.DictReader(open(sys.argv[1]))

# reads the sequence
in_file = open(sys.argv[2])
sequence = in_file.read()

# creates a dictionary for the strs
strs = {"AGATC": "0", "TTTTTTCT": "0", "AATG": "0", "TCTAG": "0", "GATA": "0", "TATC": "0", "GAAA": "0", "TCTG": "0"}

# iterates through the dictionary and the sequence looking for maximum strs
for key in strs:
    count = 0
    for i in range(len(sequence) - len(key)):
        if sequence[i:i+len(key)] == key:
            temp = 0
            for j in range(round((len(sequence) - i - len(key))/len(key))):
                if sequence[i + j*len(key): i + len(key) + j*len(key)] == key:
                    temp += 1
                else:
                    break
            if temp > count:
                count = temp
    strs[key] = str(count)

# looks whether there is a person with exact match with str counts
x = False
for row in file:
    counter = 0
    for key in row:
        if key != "name":
            if row.get(key) == strs.get(key):
                counter += 1
    if counter == len(row.items()) - 1:
        print(row["name"])
        x = True
        break

# prints no match if there isn't a match
if x == False:
    print("No match")