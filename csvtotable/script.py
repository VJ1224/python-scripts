import sqlite3
import sys
import csv
import os

if len(sys.argv) == 1:
    print("Provide filename as command line argument")
    sys.exit()

file = sys.argv[1]

if not os.path.isfile(file):
    print("File does not exist")
    sys.exit()

if file[-3:] != "csv":
    print("Not a .csv file")
    sys.exit()

with open(file, newline='') as csvFile:
    csv_reader = csv.reader(csvFile)
    headings = next(csv_reader)

    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    query = "CREATE TABLE IF NOT EXISTS data ({column_names})".format(column_names=','.join(headings))
    cursor.execute(query)

    records = []
    for row in csv_reader:
        records.append(tuple(row))
    
    vals = "("
    for column in headings:
        vals += "?,"
    vals = vals[:-1] + ")"

    cursor.executemany("INSERT INTO data VALUES {values}".format(values=vals), records)

    connection.commit()
    connection.close()