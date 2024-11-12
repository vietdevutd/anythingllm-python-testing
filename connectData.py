import psycopg2
conn = psycopg2.connect(
    host="",
    database="",
    user="",
    password="",
    port=""
)

# Add one or multiple rows
# new_values is a list of tuples. Ex: [(), (), ()]
def add(table_name, new_values):
    cur = conn.cursor()
    query = f"INSERT INTO {table_name}(name, phone_number, latest_job_title, skills, highest_education, total_years_experience, salary) \
            VALUES (%s, %s, %s, %s, %s, %s, %s);"
    cur.executemany(query, new_values)
    cur.close()


# Delete one column
def delete_one(table_name, column_name, value):
    cur = conn.cursor()
    query = f"DELETE FROM {table_name} WHERE {column_name} = %s;"
    cur.execute(query, [value])
    cur.close()

def delete_all(table_name):
    cur = conn.cursor()
    query = f"DELETE FROM {table_name}"
    cur.execute(query)
    cur.close()

# Update one or multiple columns
# updates is a dictionary
def update(table_name, updates, column_name, column_value):
    cur = conn.cursor()

    set_clause = ", ".join([f"{col} = %s" for col in updates.keys()])
    # example: set_clause = "salary = %s, total_years_experience = %s"

    # list is like an array
    values = list(updates.values())  # Values to set for the columns
    values.append(column_value)  # Add the condition value at the end
    # example: values = ['$60', 1.5, 'Google']

    # Construct the full query
    query = f"UPDATE {table_name} SET {set_clause} WHERE {column_name} = %s;"
    cur.execute(query, values)
    cur.close()

cur = conn.cursor()

conn.commit()
cur.execute("SELECT * FROM jobs;")
rows = cur.fetchall()
for row in rows:
    print(row)
cur.close()
conn.close()
