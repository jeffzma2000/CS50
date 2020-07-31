import sys
import cs50
import csv

# checks if there are 2 arguments
if (len(sys.argv) != 2):
    print("Usage: python import.py []")
    sys.exit(1)

# creates an sql database
db = cs50.SQL("sqlite:///students.db")

# opens the csv file and inserts the data into the database
with open(sys.argv[1], "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        if len(row["name"].split()) == 2:
            db.execute("INSERT INTO students (first, last, house, birth) VALUES (?, ?, ?, ?)",
                       row["name"].split()[0], row["name"].split()[1], row["house"], row["birth"])
        if len(row["name"].split()) == 3:
            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES (?, ?, ?, ?, ?)",
                       row["name"].split()[0], row["name"].split()[1], row["name"].split()[2], row["house"], row["birth"])
