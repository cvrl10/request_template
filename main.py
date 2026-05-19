import csv
import sqlite3
from datetime import datetime

conn = sqlite3.connect('database.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS lots (
    manufacturer TEXT,
    element TEXT,
    lot TEXT,
    expiration DATE
)
''')

file = open('lot.csv', mode='r', newline='')
reader = csv.DictReader(file)
for record in reader:
    try:
        cursor.execute('''
        INSERT INTO lots (manufacturer, element, lot, expiration)
        VALUES (?, ?, ?, ?)''', (record['manufacturer'], record['element'], record['lot'],
                             datetime.strptime(record['expiration'], '%b %d %Y').strftime('%Y-%m-%d')))
    except ValueError as e:
        print(e)

conn.commit()

cursor.execute('''SELECT * FROM lots''')
#cursor.execute('''SELECT * FROM lots WHERE expiration >= CURRENT_DATE''')
records = cursor.fetchall()
print(records)
