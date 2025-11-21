import sqlite3

connection = sqlite3.connect('Student.db')

cursor = connection.cursor()

# Drop table if exists to avoid errors on re-run
cursor.execute("DROP TABLE IF EXISTS STUDENT")

table_info = '''
CREATE TABLE STUDENT(
    NAME VARCHAR(50),
    AGE INT,
    CLASS VARCHAR(10),
    SECTION VARCHAR(5),
    MARKS INT,
    SUBJECT VARCHAR(30),
    ATTENDANCE FLOAT,
    CITY VARCHAR(30)
);
'''

cursor.execute(table_info)

# Rich dataset with 30+ students
students = [
    ('Alice Johnson', 14, '8th', 'A', 85, 'Mathematics', 92.5, 'New York'),
    ('Bob Smith', 15, '9th', 'B', 92, 'Science', 88.3, 'Los Angeles'),
    ('Charlie Brown', 13, '7th', 'A', 78, 'English', 95.0, 'Chicago'),
    ('Diana Prince', 14, '8th', 'B', 88, 'Mathematics', 90.2, 'Houston'),
    ('Eve Williams', 15, '9th', 'A', 95, 'Science', 97.8, 'Phoenix'),
    ('Frank Miller', 13, '7th', 'B', 72, 'English', 85.5, 'Philadelphia'),
    ('Grace Lee', 14, '8th', 'A', 91, 'Mathematics', 93.1, 'San Antonio'),
    ('Henry Davis', 15, '9th', 'B', 83, 'Science', 89.0, 'San Diego'),
    ('Ivy Chen', 13, '7th', 'A', 89, 'English', 96.4, 'Dallas'),
    ('Jack Wilson', 14, '8th', 'B', 76, 'Mathematics', 82.7, 'San Jose'),
    ('Kate Anderson', 15, '9th', 'A', 94, 'Science', 91.5, 'Austin'),
    ('Liam Taylor', 13, '7th', 'B', 81, 'English', 87.9, 'Jacksonville'),
    ('Mia Garcia', 14, '8th', 'A', 87, 'Mathematics', 94.3, 'Fort Worth'),
    ('Noah Martinez', 15, '9th', 'B', 90, 'Science', 86.2, 'Columbus'),
    ('Olivia Rodriguez', 13, '7th', 'A', 93, 'English', 98.1, 'Charlotte'),
    ('Peter Hernandez', 14, '8th', 'B', 79, 'Mathematics', 83.6, 'San Francisco'),
    ('Quinn Lopez', 15, '9th', 'A', 96, 'Science', 95.7, 'Indianapolis'),
    ('Rachel Gonzalez', 13, '7th', 'B', 84, 'English', 90.0, 'Seattle'),
    ('Sam Wilson', 14, '8th', 'A', 88, 'Mathematics', 92.8, 'Denver'),
    ('Tina Perez', 15, '9th', 'B', 91, 'Science', 89.5, 'Washington'),
    ('Uma Sanchez', 13, '7th', 'A', 86, 'English', 94.2, 'Boston'),
    ('Victor Torres', 14, '8th', 'B', 82, 'Mathematics', 88.1, 'Nashville'),
    ('Wendy Rivera', 15, '9th', 'A', 97, 'Science', 96.9, 'Detroit'),
    ('Xavier Flores', 13, '7th', 'B', 77, 'English', 84.3, 'Portland'),
    ('Yara Cruz', 14, '8th', 'A', 90, 'Mathematics', 93.5, 'Las Vegas'),
    ('Zack Diaz', 15, '9th', 'B', 85, 'Science', 87.4, 'Memphis'),
    ('Amy Reyes', 13, '7th', 'A', 92, 'English', 97.2, 'Louisville'),
    ('Brian Morales', 14, '8th', 'B', 80, 'Mathematics', 85.9, 'Baltimore'),
    ('Chloe Jimenez', 15, '9th', 'A', 98, 'Science', 99.0, 'Milwaukee'),
    ('David Ruiz', 13, '7th', 'B', 75, 'English', 82.5, 'Albuquerque'),
]

cursor.executemany(
    "INSERT INTO STUDENT (NAME, AGE, CLASS, SECTION, MARKS, SUBJECT, ATTENDANCE, CITY) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
    students
)

connection.commit()

print("Data inserted successfully")
print(f"Total records: {len(students)}")

data = cursor.execute("SELECT * FROM STUDENT")
for row in data:
    print(row)

connection.close()