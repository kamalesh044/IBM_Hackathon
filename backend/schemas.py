from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


# Student Schemas
class StudentBase(BaseModel):
    student_id: str = Field(..., min_length=1, max_length=50)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    grade_level: Optional[str] = Field(None, max_length=20)


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    grade_level: Optional[str] = Field(None, max_length=20)
    is_active: Optional[bool] = None


class StudentResponse(StudentBase):
    id: int
    enrollment_date: datetime
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Assessment Schemas
class AssessmentBase(BaseModel):
    assessment_type: str = Field(..., min_length=1, max_length=50)
    subject: str = Field(..., min_length=1, max_length=100)
    score: float = Field(..., ge=0)
    max_score: float = Field(..., gt=0)
    assessment_date: datetime
    notes: Optional[str] = None


class AssessmentCreate(AssessmentBase):
    student_id: int


class AssessmentUpdate(BaseModel):
    assessment_type: Optional[str] = Field(None, min_length=1, max_length=50)
    subject: Optional[str] = Field(None, min_length=1, max_length=100)
    score: Optional[float] = Field(None, ge=0)
    max_score: Optional[float] = Field(None, gt=0)
    assessment_date: Optional[datetime] = None
    notes: Optional[str] = None


class AssessmentResponse(AssessmentBase):
    id: int
    student_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Analytics Schemas
class StudentAnalyticsBase(BaseModel):
    risk_level: Optional[str] = Field(None, max_length=20)
    predicted_performance: Optional[float] = Field(None, ge=0, le=100)
    engagement_score: Optional[float] = Field(None, ge=0, le=100)
    attendance_rate: Optional[float] = Field(None, ge=0, le=100)
    recommendation: Optional[str] = None


class StudentAnalyticsCreate(StudentAnalyticsBase):
    student_id: int


class StudentAnalyticsResponse(StudentAnalyticsBase):
    id: int
    student_id: int
    analysis_date: datetime
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Pagination Schema
class PaginatedResponse(BaseModel):
    items: list
    total: int
    page: int
    page_size: int
    total_pages: int
