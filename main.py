import sqlite3
import os

def print_instructions():
    print('1 - Показати список студентів')
    print('2 - Показати список курсів')
    print("3 - Додати нового студента")
    print("4 - Додати новий курс")
    print("5 - Зареєструвати студента на курс")
    print("6 - Показати студентів певного курса")

def show_students(cursor):
    result = cursor.execute("""
    SELECT name, age, major FROM students        
    """)
    student = result.fetchone()
    while student:
        print(f'{student[0]}, {student[1]} років: {student[2]}')
        student = result.fetchone()

def show_courses(cursor):
    result = cursor.execute("""
    SELECT course_name, instructor FROM courses
    """)
    course = result.fetchone()
    while course:
        print(f'Курс {course[0]}, інструктор {course[1]}')
        course = result.fetchone()

def show_specific_course(cursor):
    course_name = input("Назва курсу: "),
    result = cursor.execute("""
    SELECT students.name
    FROM students, courses, students_course
    WHERE courses.course_name = ?
    AND courses.course_id = students_course.course_id
    AND students_course.student_id = students.id
    """, (course_name))
    student_name = result.fetchone()
    while student_name:
        print(student_name[0])
        student_name = result.fetchone()

def add_new_course(con, cursor):
    course_name = input("Назва курсу: ")
    instructor = input("Ім'я інструктора: ")
    params = (course_name, instructor)
    cursor.execute("""
    INSERT INTO courses (course_name, instructor)
    VALUES
    (?, ?)
    """, params)
    con.commit()
    print("Курс додано!")

def add_new_student(con, cursor):
    name = input("Ім'я студента: ")
    age = int(input("Вік студента: "))
    major = input("Головний предмет студента: ")
    params = (name, age, major)
    cursor.execute('INSERT INTO students (name, age, major) VALUES (?, ?, ?)', params)
    con.commit()
    print("Учня додано!")

def register_student_for_course(con, cursor):
    name = input("Ім'я студента: ")
    course_name = input("Назва курсу: ")
    params = (name, course_name)
    ids = cursor.execute("""
    SELECT students.id, courses.course_id
    FROM students, courses
    WHERE students.name == ? AND courses.course_name = ?
    LIMIT 1
    """, params).fetchone()

    cursor.execute("""
    INSERT INTO students_course (student_id, course_id)
    VALUES
    (?, ?)
    """, ids)

    con.commit()
    print("Студента зареєстровано!")

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

while True:
    feedback = input("Введіть 'help' для інструкцій.\n")
    if feedback == "help":
        print_instructions()
    elif feedback == "1":
        show_students(cursor)
    elif feedback == "2":
        show_courses(cursor)
    elif feedback == "3":
        add_new_student(con, cursor)
    elif feedback == "4":
        add_new_course(con, cursor)
    elif feedback == "5":
        register_student_for_course(con, cursor)
    elif feedback == "6":
        show_specific_course(cursor)
    elif not feedback:
        break