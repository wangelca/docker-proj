from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    studentID = Column(String, unique=True, index=True)
    studentName = Column(String)
    course = Column(String)
    presentDate = Column(String)

Base.metadata.create_all(bind=engine)
print("Tables created successfully!")

class StudentCreate(BaseModel):
    studentID: str
    studentName: str
    course: str
    presentDate: str

@app.post("/student")
def create_student(student: StudentCreate):
    db = SessionLocal()
    db_student = db.query(Student).filter(Student.studentID == student.studentID).first()
    if db_student:
        raise HTTPException(status_code=409, detail="Student already exists")
    new_student = Student(**student.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student
