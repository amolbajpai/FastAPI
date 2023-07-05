from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm.session import Session
from typing import Optional




# SQLite database URL
DATABASE_URL = "sqlite:///./students.db"

# Create the engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()

# Define the ORM model for the student
class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    roll_no = Column(String)
    address = Column(String)

# Create the tables in the database
Base.metadata.create_all(bind=engine)

# Define the data model for the student
class StudentCreate(BaseModel):
    name: str
    roll_no: str
    address: str




class StudentUpdate(BaseModel):
    name: str
    roll_no: str
    address: str

class StudentUpdatePatch(BaseModel):
    name: Optional[str]
    roll_no: Optional[str]
    address: Optional[str]

# Create the FastAPI application
app = FastAPI()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to create a new student
@app.post("/students")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = Student(name=student.name, roll_no=student.roll_no, address=student.address)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return {"message": "Student created successfully"}

# Endpoint to get all students
@app.get("/students")
def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return students

# Endpoint to get a specific student by ID
@app.get("/students/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# Endpoint to update a specific student by ID
@app.put("/students/{student_id}")
def update_student(student_id: int, student: StudentUpdate, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    db_student.name = student.name
    db_student.roll_no = student.roll_no
    db_student.address = student.address
    db.commit()
    db.refresh(db_student)
    return {"message": "Student updated successfully"}


# Endpoint to partially update a specific student by ID
@app.patch("/students/{student_id}")
def partially_update_student(student_id: int, student: StudentUpdatePatch, db: Session = Depends(get_db)):
    print(student)
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    if student.name:
        db_student.name = student.name
    if student.roll_no:
        db_student.roll_no = student.roll_no
    if student.address:
        db_student.address = student.address
    db.commit()
    db.refresh(db_student)
    return {"message": "Student partially updated successfully"}


# # Endpoint to partially update a specific student by ID
# @app.patch("/students/{student_id}")
# def partially_update_student(student_id: int, student: StudentUpdate, db: Session = Depends(get_db)):
#     db_student = db.query(Student).filter(Student.id == student_id).first()
#     if not db_student:
#         raise HTTPException(status_code=404, detail="Student not found")

#     student_data = student.dict(exclude_unset=True)
#     for key, value in student_data.items():
#         setattr(db_student, key, value)

#     db.commit()
#     db.refresh(db_student)
#     return {"message": "Student partially updated successfully"}



# Endpoint to delete a specific student by ID
@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(db_student)
    db.commit()
    return {"message": "Student deleted successfully"}
