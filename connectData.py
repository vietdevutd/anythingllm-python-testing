import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="bomhacpro",
    port="3000"
)
cur = conn.cursor()
cur.execute("SELECT * FROM jobdesc;")
rows = cur.fetchall()

for row in rows:
    print(row)
