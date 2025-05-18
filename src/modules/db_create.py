import sqlite3,csv

conn = sqlite3.Connection('main.db')
cur = conn.cursor()

cur.execute("CREATE TABLE sites(Domain, Status_code, Description, Response_time,Page_exists, Tag_count, Score)")
conn.commit()

with open('test/BTCL.csv', 'r') as csv_file:  # Replace 'domains.csv' with your CSV file name
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        domain = row['Domain']  # Replace 'Domain' with the exact column name in your CSV
        cur.execute('INSERT INTO sites (Domain) VALUES (?)', (domain,))

# Commit changes and close the connection
conn.commit()
conn.close()