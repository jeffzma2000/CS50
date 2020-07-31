import sys
import cs50
import csv

# checks if there are 2 arguments
if (len(sys.argv) != 2):
    print("Usage: python import.py []")
    sys.exit(1)

# opens an sql database
db = cs50.SQL("sqlite:///students.db")

# sees what house the user put
house = sys.argv[1]

# gets information from database on people in that house
first = db.execute("SELECT first FROM students WHERE house = ? ORDER BY last", house)
middle = db.execute("SELECT middle FROM students WHERE house = ? ORDER BY last", house)
last = db.execute("SELECT last FROM students WHERE house = ? ORDER BY last", house)
year = db.execute("SELECT birth FROM students WHERE house = ? ORDER BY last", house)

# prints out the information of who is in the house
for i in range(len(first)):
    if middle[i]["middle"] == None:
        print("{} {}, born {}".format(first[i]["first"], last[i]["last"], year[i]["birth"]))
    else:
        print("{} {} {}, born {}".format(first[i]["first"], middle[i]["middle"], last[i]["last"], year[i]["birth"]))
