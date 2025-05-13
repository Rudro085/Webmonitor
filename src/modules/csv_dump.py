import sqlite3
import csv

conn = sqlite3.Connection('main.db')
cur = conn.cursor()

cur.execute("SELECT * FROM sites")
rows = cur.fetchall()

with open('sites_dump.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    # Write header
    column_names = [description[0] for description in cur.description]
    csvwriter.writerow(column_names)
    # Write data
    csvwriter.writerows(rows)

print("Data has been dumped into sites_dump.csv")
