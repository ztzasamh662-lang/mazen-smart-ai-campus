import psycopg2
from config import DB_CONFIG

conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

cur.execute("SELECT id, name FROM persons;")
rows = cur.fetchall()

if rows:
    print("Students in database:")
    for r in rows:
        print(r)
else:
    print("No students found in the database!")

cur.close()
conn.close()