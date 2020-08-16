#!/usr/bin/env python3
import mysql.connector
import csv
import os.path
import sys

if __name__ == "__main__":
    csvfile = os.path.join(sys.path[0], "zuordnung_plz_ort_landkreis_sorted.csv")
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="besuchertracker"
    )
    cursor = db.cursor(prepared=True)
    insert_stmt = "INSERT INTO landkreise (id, plz, landkreis, bundesland) VALUES (%s, %s, %s, %s)"
    with open(csvfile, mode='r') as c:
        r = csv.reader(c)
        next(r) # skip header
        for i, row in enumerate(r):
            cursor.execute(insert_stmt, (i, row[3], row[4], row[5]))
    db.commit()
