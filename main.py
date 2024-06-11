import uvicorn
from datetime import date
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Import our tools
# This is the database connection file
from sqlmodel import Session, select, func, literal_column
from db import get_session

# These are our models
from models.students import Students
from models.courses import Courses
from models.enrollments import Enrollments

app = FastAPI()

# Setup our origins...
# ...for now it's just our local environments
origins = [
    "http://localhost",
    "http://localhost:3000",
]

# Add the CORS middleware...
# ...this will pass the proper CORS headers
# https://fastapi.tiangolo.com/tutorial/middleware/
# https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Root Route"}


@app.get('/courses')
def get_courses(session: Session = Depends(get_session)):
    courses = session.query(Courses)
    return courses.all()


@app.get('/students')
def get_students(session: Session = Depends(get_session)):
    students = session.query(Students)
    return students.all()


@app.get('/enrollments/courses')
def get_enrollments(session: Session = Depends(get_session)):
    statement = select(
        Courses.name.label('course_name'),
        func.array_agg(Students.name).label('students')
    ).select_from(
        Enrollments
    ).join(
        Students, Students.id == Enrollments.student_id
    ).join(
        Courses, Courses.id == Enrollments.course_id
    ).group_by(
        Courses.id,
        Courses.name
    )

    enrollments = session.exec(statement).mappings().all()
    print(f"Enrollments SQL: {enrollments}")
    return enrollments


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)
