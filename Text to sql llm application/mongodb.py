from pymongo import MongoClient
import sqlite3

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['text_to_sql']  # Changed database name
collection = db['students']

# Clear existing data
collection.delete_many({})

# Connect to SQLite and migrate data
conn = sqlite3.connect('Student.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM STUDENT")
rows = cursor.fetchall()

# Convert to MongoDB documents
students = []
for row in rows:
    student = {
        "name": row[0],
        "age": row[1],
        "class": row[2],
        "section": row[3],
        "marks": row[4],
        "subject": row[5],
        "attendance": row[6],
        "city": row[7]
    }
    students.append(student)

# Insert into MongoDB
if students:
    collection.insert_many(students)
    print(f"✅ Inserted {len(students)} students into MongoDB")
    print(f"📊 Database: text_to_sql")
    print(f"📁 Collection: students")

conn.close()
client.close()