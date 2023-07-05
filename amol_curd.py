from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Create a table for storing student information
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        roll_no TEXT,
        address TEXT
    )
""")
conn.commit()

# Define the data model for the student
class Student(BaseModel):
    name: str
    roll_no: str
    address: str

# Create the FastAPI application
app = FastAPI()

# Endpoint to create a new student
@app.post("/students")
async def create_student(student: Student):
    cursor.execute("""
        INSERT INTO students (name, roll_no, address)
        VALUES (?, ?, ?)
    """, (student.name, student.roll_no, student.address))
    conn.commit()
    return {"message": "Student created successfully"}

# Endpoint to get all students
@app.get("/students")
async def get_students():
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    students = []
    for row in rows:
        student = {
            "id": row[0],
            "name": row[1],
            "roll_no": row[2],
            "address": row[3]
        }
        students.append(student)
    return students

# Endpoint to get a specific student by ID
@app.get("/students/{student_id}")
async def get_student(student_id: int):
    cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))
    row = cursor.fetchone()
    if row is None:
        return {"message": "Student not found"}
    student = {
        "id": row[0],
        "name": row[1],
        "roll_no": row[2],
        "address": row[3]
    }
    return student

# Endpoint to update a specific student by ID
@app.put("/students/{student_id}")
async def update_student(student_id: int, student: Student):
    cursor.execute("""
        UPDATE students
        SET name=?, roll_no=?, address=?
        WHERE id=?
    """, (student.name, student.roll_no, student.address, student_id))
    conn.commit()
    return {"message": "Student updated successfully"}

# Endpoint to delete a specific student by ID
@app.delete("/students/{student_id}")
async def delete_student(student_id: int):
    cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()
    return {"message": "Student deleted successfully"}
