import sqlite3
import os

PATH = os.path.dirname(__file__) + os.sep

con = sqlite3.connect(PATH + 'students.db')
cursor = con.cursor()

cursor.execute(""" 
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(256),
    age INTEGER,
    major VARCHAR(256)
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name VARCHAR(256),
    instructor VARCHAR(256)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS students_course (
    student_id INTEGER,
    course_id INTEGER,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    PRIMARY KEY (student_id, course_id)
)     
""")