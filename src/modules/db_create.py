import sqlite3,csv

conn = sqlite3.Connection('main.db')
cur = conn.cursor()

cur.execute("CREATE TABLE sites(Domain, Status_code, Description, SSL, Response_time, Browser_status, Page_exists, Tag_count, Score)")
conn.commit()

with open('site_dump2.csv', 'r') as csv_file:  
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        domain = row['Domains'] 
        cur.execute('INSERT INTO sites (Domain) VALUES (?)', (domain,))

conn.commit()
conn.close()