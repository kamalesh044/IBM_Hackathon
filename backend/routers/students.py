from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from backend.database import get_db
from backend.models import Student, Assessment
from backend.schemas import (
    StudentCreate,
    StudentUpdate,
    StudentResponse,
    AssessmentCreate,
    AssessmentUpdate,
    AssessmentResponse
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    """Create a new student"""
    try:
        # Check if student_id already exists
        existing = db.query(Student).filter(Student.student_id == student.student_id).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Student with ID {student.student_id} already exists"
            )
        
        # Check if email already exists
        existing_email = db.query(Student).filter(Student.email == student.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Student with email {student.email} already exists"
            )
        
        db_student = Student(**student.model_dump())
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        logger.info(f"Created student: {db_student.student_id}")
        return db_student
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating student: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create student"
        )


@router.get("/", response_model=List[StudentResponse])
def get_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    is_active: Optional[bool] = None,
    grade_level: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of students with optional filters"""
    try:
        query = db.query(Student)
        
        if is_active is not None:
            query = query.filter(Student.is_active == is_active)
        
        if grade_level:
            query = query.filter(Student.grade_level == grade_level)
        
        students = query.offset(skip).limit(limit).all()
        return students
    except Exception as e:
        logger.error(f"Error fetching students: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch students"
        )


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    """Get a specific student by ID"""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found"
        )
    return student


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student_update: StudentUpdate,
    db: Session = Depends(get_db)
):
    """Update a student's information"""
    try:
        db_student = db.query(Student).filter(Student.id == student_id).first()
        if not db_student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with ID {student_id} not found"
            )
        
        update_data = student_update.model_dump(exclude_unset=True)
        
        # Check email uniqueness if being updated
        if "email" in update_data:
            existing = db.query(Student).filter(
                Student.email == update_data["email"],
                Student.id != student_id
            ).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Email {update_data['email']} is already in use"
                )
        
        for field, value in update_data.items():
            setattr(db_student, field, value)
        
        db.commit()
        db.refresh(db_student)
        logger.info(f"Updated student: {db_student.student_id}")
        return db_student
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating student: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update student"
        )


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    """Delete a student"""
    try:
        db_student = db.query(Student).filter(Student.id == student_id).first()
        if not db_student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with ID {student_id} not found"
            )
        
        db.delete(db_student)
        db.commit()
        logger.info(f"Deleted student: {db_student.student_id}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting student: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete student"
        )


@router.post("/{student_id}/assessments", response_model=AssessmentResponse, status_code=status.HTTP_201_CREATED)
def create_assessment(
    student_id: int,
    assessment: AssessmentCreate,
    db: Session = Depends(get_db)
):
    """Create a new assessment for a student"""
    try:
        # Verify student exists
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with ID {student_id} not found"
            )
        
        assessment_data = assessment.model_dump()
        assessment_data["student_id"] = student_id
        
        db_assessment = Assessment(**assessment_data)
        db.add(db_assessment)
        db.commit()
        db.refresh(db_assessment)
        logger.info(f"Created assessment for student {student_id}")
        return db_assessment
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating assessment: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create assessment"
        )


@router.get("/{student_id}/assessments", response_model=List[AssessmentResponse])
def get_student_assessments(
    student_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all assessments for a specific student"""
    try:
        # Verify student exists
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with ID {student_id} not found"
            )
        
        assessments = db.query(Assessment).filter(
            Assessment.student_id == student_id
        ).offset(skip).limit(limit).all()
        
        return assessments
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching assessments: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch assessments"
        )
