import csv
import sqlite3
from datetime import datetime
import sys

file = open('stdout_err.log', mode='w')
sys.stdout = file
sys.stderr = file

def query_database(elements):
    lot = {}
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''DROP TABLE IF EXISTS lots;''')
    cursor.execute('''
    CREATE TABLE lots (
        manufacturer TEXT,
        element TEXT,
        lot TEXT,
        expiration DATE     
    );
    ''')
    try:
        file = open('lot.csv', mode='r', newline='')
        reader = csv.DictReader(file)
        for record in reader:
            for date_format in ['%b %d %Y', '%B %d %Y']: #note MAY matches twice but that's OK
                try:
                    cursor.execute('''
                    INSERT INTO lots (manufacturer, element, lot, expiration)
                    VALUES (?, ?, ?, ?);''', (record['manufacturer'], record['element'], record['lot'],
                                                        datetime.strptime(record['expiration'], date_format).strftime('%Y-%m-%d')))
                except (ValueError, sqlite3.IntegrityError) as e:
                    print(e)

        conn.commit()
        placeholders = ', '.join('?' for _ in elements)
        cursor.execute(f'''SELECT element, manufacturer, lot, expiration 
                               FROM lots 
                               WHERE expiration >= CURRENT_DATE
                               AND element COLLATE NOCASE IN ({placeholders});''', elements)

        records = cursor.fetchall()
        file.close()

        for record in records:
            lot.update({record[0].lower(): f'Manufacturer: {record[1]}, {record[2]} exp: {record[3]}'})
    except FileNotFoundError as e:
        print(e)
    finally:
        conn.close()

    return lot

