from fastapi import FastAPI, Path
from pydantic import BaseModel
from fastapi import HTTPException
from pydantic import BaseModel


app = FastAPI()

students = {
    1 : {
        "name" : "john",
        "age" : 14,
        "class" : 21
    }
}

class Student(BaseModel):
    name : str
    age : int
    year : str


@app.get("/")
async def index():
    return {"name" : "First Data"}

@app.get("/get-student/{student_id}")
async def get_student(student_id : int = Path(description= "The id of the student you want to view",gt=0,lt=2)):
    return students[student_id]

@app.get("/get-by-name")
async def get_student(name : str):
    for student_id in students:
        if students[student_id]['name'] == name:
            return students[student_id]
    return {"Data" : "Not found"}


@app.post("/create-student/{student_id}")
async def crete_student(student_id :int, student : Student):
    if student_id in students:
        return {"Error" : "student existes"}
    students[student_id] = student
    return students[student_id]