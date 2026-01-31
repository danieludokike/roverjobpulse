
import sqlite3

conn = sqlite3.connect("roverjobpulse.db")
cursor = conn.cursor()

for row in cursor.execute("SELECT title, company FROM jobs LIMIT 5"):
    print(row)

conn.close()
