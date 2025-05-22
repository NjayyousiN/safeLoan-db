from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
from db.session import get_db
from db.CRUD import create_course, get_course, get_all_courses, update_course, delete_course
from schemas.course import CourseUpdate, CourseResponse
import shutil
import os
from datetime import datetime
from pathlib import Path

UPLOAD_DIR = "uploads/"

router = APIRouter(
    prefix="/courses",
    tags=["courses"]
)

# Create a new course
@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_new_course(
    field: str,
    subject: str | None = None,
    class_timing: str | None = None,
    instructor_name: str | None = None,
    course_pic: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    # Handle file upload if provided
    course_pic_path = None
    if course_pic:
        # Create unique filename using timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = os.path.splitext(course_pic.filename)[1]
        filename = f"course_{field}_{timestamp}{file_extension}"
        # Ensure upload directory exists
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_path = os.path.join(UPLOAD_DIR, filename)


        # Save the file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(course_pic.file, buffer)
        
        course_pic_path = str(file_path)

    # Create course with file path
    return create_course(
        db=db,
        field=field,
        subject=subject,
        class_timing=class_timing,
        instructor_name=instructor_name,
        course_pic=course_pic_path
    )

# Get course by ID
@router.get("/{course_id}", response_model=CourseResponse)
async def get_course_by_id(
    course_id: int,
    db: Session = Depends(get_db)
):
    db_course = get_course(db, course_id)
    if db_course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {course_id} not found"
        )
    return db_course

# Get all courses with pagination
@router.get("/", response_model=List[CourseResponse])
async def get_courses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return get_all_courses(db, skip=skip, limit=limit)

# Get course image by name
@router.get("/images/{image_name}")
async def get_image(image_name: str):
    file_path = f"uploads/{image_name}"
    return FileResponse(
        file_path,
        media_type="image/jpeg", 
        filename=image_name
    )


# Update course by ID
@router.put("/{course_id}", response_model=CourseResponse)
async def update_course_by_id(
    course_id: int,
    course: CourseUpdate,
    db: Session = Depends(get_db)
):
    db_course = update_course(db, course_id, **course.model_dump(exclude_unset=True))
    if db_course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {course_id} not found"
        )
    return db_course

# Delete course by ID
@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course_by_id(
    course_id: int,
    db: Session = Depends(get_db)
):
    success = delete_course(db, course_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {course_id} not found"
        )
    return None