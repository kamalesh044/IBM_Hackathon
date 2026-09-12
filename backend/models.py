from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class Student(Base):
    """Student model for storing student information"""
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(50), unique=True, index=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    grade_level = Column(String(20))
    enrollment_date = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    assessments = relationship("Assessment", back_populates="student", cascade="all, delete-orphan")
    analytics = relationship("StudentAnalytics", back_populates="student", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Student {self.student_id}: {self.first_name} {self.last_name}>"


class Assessment(Base):
    """Assessment model for storing student assessment data"""
    __tablename__ = "assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    assessment_type = Column(String(50), nullable=False)  # quiz, test, assignment, project
    subject = Column(String(100), nullable=False)
    score = Column(Float, nullable=False)
    max_score = Column(Float, nullable=False)
    assessment_date = Column(DateTime, nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="assessments")
    
    def __repr__(self):
        return f"<Assessment {self.id}: {self.subject} - {self.score}/{self.max_score}>"


class StudentAnalytics(Base):
    """Student analytics model for storing predictive insights"""
    __tablename__ = "student_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    risk_level = Column(String(20))  # low, medium, high
    predicted_performance = Column(Float)
    engagement_score = Column(Float)
    attendance_rate = Column(Float)
    recommendation = Column(Text)
    analysis_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="analytics")
    
    def __repr__(self):
        return f"<StudentAnalytics {self.id}: Student {self.student_id} - Risk: {self.risk_level}>"
