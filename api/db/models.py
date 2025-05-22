from sqlalchemy import Column, Integer, String, Date, Text, DateTime, func, Table, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


students_courses = Table(
    'students_courses',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id'), primary_key=True),
    Column('course_id', Integer, ForeignKey('courses.id'), primary_key=True),
)

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True, nullable=False)
    name = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    courses = relationship('Course', secondary=students_courses, back_populates='students')

    def __repr__(self):
        return f"<User(id={self.id}, username={self.name}, email={self.email})>"
    
class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True, nullable=False)
    field = Column(String(50), nullable=False)
    subject = Column(Text, nullable=True)
    class_timing = Column(String(50), nullable=True)
    no_of_registered_students = Column(Integer, default=0)
    instructor_name = Column(String(50), nullable=True)
    course_pic = Column(String(255), nullable=True)

    students = relationship('Student', secondary=students_courses, back_populates='courses')

    def __repr__(self):
        return f"<Course(id={self.id}, name={self.field}, subject={self.subject})>"