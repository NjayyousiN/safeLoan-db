from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from db.models import Student, Course

# Student CRUD Operations
def create_student(db: Session, name: str, email: str, password: str):
    db_student = Student(
        name=name,
        email=email,
        password=password  
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_student(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()

def get_student_by_email(db: Session, email: str):
    return db.query(Student).filter(Student.email == email).first()

# def get_all_students(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(Student).offset(skip).limit(limit).all()

# def update_student(db: Session, student_id: int, **kwargs):
#     db_student = db.query(Student).filter(Student.id == student_id).first()
#     if db_student:
#         for key, value in kwargs.items():
#             setattr(db_student, key, value)
#         db.commit()
#         db.refresh(db_student)
#     return db_student

def delete_student(db: Session, student_id: int):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student:
        db.delete(db_student)
        db.commit()
        return True
    return False

# Course CRUD Operations
def create_course(db: Session, field: str, subject: Optional[str] = None, 
                 class_timing: Optional[str] = None, instructor_name: Optional[str] = None, course_pic: Optional[str] = None):
    db_course = Course(
        field=field,
        subject=subject,
        class_timing=class_timing,
        instructor_name=instructor_name,
        course_pic=course_pic,

    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def get_course(db: Session, course_id: int):
    return db.query(Course).filter(Course.id == course_id).first()

def get_all_courses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Course).offset(skip).limit(limit).all()

def update_course(db: Session, course_id: int, **kwargs):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course:
        for key, value in kwargs.items():
            setattr(db_course, key, value)
        db.commit()
        db.refresh(db_course)
    return db_course

def delete_course(db: Session, course_id: int):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course:
        db.delete(db_course)
        db.commit()
        return True
    return False

# Student-Course Relationship Operations
def enroll_student_in_course(db: Session, student_id: int, course_id: int):
    student = get_student(db, student_id)
    course = get_course(db, course_id)
    
    if student and course:
        student.courses.append(course)
        course.no_of_registered_students += 1
        db.commit()
        return True
    return False

def unenroll_student_from_course(db: Session, student_id: int, course_id: int):
    student = get_student(db, student_id)
    course = get_course(db, course_id)
    
    if student and course and course in student.courses:
        student.courses.remove(course)
        course.no_of_registered_students -= 1
        db.commit()
        return True
    return False