import sys

if len(sys.argv) != 3:
    sys.exit("Usage: python dna.py infile outfile")

file = open(sys.argv[1])
contents = file.read()