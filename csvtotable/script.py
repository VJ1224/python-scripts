import sqlite3
import sys
import csv
import os

def main():
    if len(sys.argv) == 1:
        print("Provide filename as command line argument")
        return

    file = sys.argv[1]

    if not os.path.isfile(file):
        print("File does not exist")
        return

    if file[-3:] != "csv":
        print("Not a .csv file")
        return

    with open(file, newline='', encoding='utf-8') as csvFile:
        csv_reader = csv.reader(csvFile)
        headings = next(csv_reader)
        
        database_name = file[:-3] + ".db"
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()

        query = "CREATE TABLE IF NOT EXISTS data ({column_names})".format(column_names=','.join(headings))
        cursor.execute(query)
        print("Table Created")

        records = []
        for row in csv_reader:
            records.append(tuple(row))
        
        vals = "("
        for column in headings:
            vals += "?,"
        vals = vals[:-1] + ")"

        cursor.executemany("INSERT INTO data VALUES {values}".format(values=vals), records)
        print("Values inserted")

        connection.commit()
        connection.close()
        print("Done")

if __name__ == "__main__":
    main()