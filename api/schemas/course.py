from pydantic import BaseModel
from typing import Optional

class CourseBase(BaseModel):
    field: str
    subject: Optional[str] = None
    class_timing: Optional[str] = None
    instructor_name: Optional[str] = None


class CourseUpdate(BaseModel):
    field: Optional[str] = None
    subject: Optional[str] = None
    class_timing: Optional[str] = None
    instructor_name: Optional[str] = None
    no_of_registered_students: Optional[int] = None

class CourseResponse(CourseBase):
    id: int
    no_of_registered_students: int
    course_pic: Optional[str] = None

    class Config:
        from_attributes = True