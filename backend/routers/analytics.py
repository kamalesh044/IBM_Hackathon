from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from datetime import datetime, timedelta
import logging

from backend.database import get_db
from backend.models import Student, Assessment, StudentAnalytics
from backend.schemas import StudentAnalyticsCreate, StudentAnalyticsResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/", response_model=StudentAnalyticsResponse, status_code=status.HTTP_201_CREATED)
def create_analytics(analytics: StudentAnalyticsCreate, db: Session = Depends(get_db)):
    """Create analytics record for a student"""
    try:
        # Verify student exists
        student = db.query(Student).filter(Student.id == analytics.student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with ID {analytics.student_id} not found"
            )
        
        db_analytics = StudentAnalytics(**analytics.model_dump())
        db.add(db_analytics)
        db.commit()
        db.refresh(db_analytics)
        logger.info(f"Created analytics for student {analytics.student_id}")
        return db_analytics
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating analytics: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create analytics"
        )


@router.get("/student/{student_id}", response_model=List[StudentAnalyticsResponse])
def get_student_analytics(
    student_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get analytics history for a specific student"""
    try:
        # Verify student exists
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with ID {student_id} not found"
            )
        
        analytics = db.query(StudentAnalytics).filter(
            StudentAnalytics.student_id == student_id
        ).order_by(desc(StudentAnalytics.analysis_date)).offset(skip).limit(limit).all()
        
        return analytics
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching analytics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch analytics"
        )


@router.get("/student/{student_id}/latest", response_model=StudentAnalyticsResponse)
def get_latest_analytics(student_id: int, db: Session = Depends(get_db)):
    """Get the most recent analytics for a student"""
    try:
        # Verify student exists
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with ID {student_id} not found"
            )
        
        analytics = db.query(StudentAnalytics).filter(
            StudentAnalytics.student_id == student_id
        ).order_by(desc(StudentAnalytics.analysis_date)).first()
        
        if not analytics:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No analytics found for student {student_id}"
            )
        
        return analytics
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching latest analytics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch latest analytics"
        )


@router.get("/risk-summary")
def get_risk_summary(db: Session = Depends(get_db)):
    """Get summary of students by risk level"""
    try:
        # Get latest analytics for each student
        subquery = db.query(
            StudentAnalytics.student_id,
            func.max(StudentAnalytics.analysis_date).label('max_date')
        ).group_by(StudentAnalytics.student_id).subquery()
        
        latest_analytics = db.query(StudentAnalytics).join(
            subquery,
            (StudentAnalytics.student_id == subquery.c.student_id) &
            (StudentAnalytics.analysis_date == subquery.c.max_date)
        ).all()
        
        risk_counts = {"low": 0, "medium": 0, "high": 0, "unknown": 0}
        
        for analytics in latest_analytics:
            risk_level = analytics.risk_level.lower() if analytics.risk_level else "unknown"
            if risk_level in risk_counts:
                risk_counts[risk_level] += 1
            else:
                risk_counts["unknown"] += 1
        
        return {
            "total_students_analyzed": len(latest_analytics),
            "risk_distribution": risk_counts,
            "timestamp": datetime.utcnow()
        }
    except Exception as e:
        logger.error(f"Error generating risk summary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate risk summary"
        )


@router.get("/student/{student_id}/performance-trend")
def get_performance_trend(
    student_id: int,
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Get performance trend for a student over specified days"""
    try:
        # Verify student exists
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with ID {student_id} not found"
            )
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        assessments = db.query(Assessment).filter(
            Assessment.student_id == student_id,
            Assessment.assessment_date >= cutoff_date
        ).order_by(Assessment.assessment_date).all()
        
        if not assessments:
            return {
                "student_id": student_id,
                "period_days": days,
                "assessments_count": 0,
                "average_score": None,
                "trend": "insufficient_data"
            }
        
        # Calculate average score percentage
        total_percentage = sum((a.score / a.max_score * 100) for a in assessments)
        average_score = total_percentage / len(assessments)
        
        # Simple trend calculation (compare first half vs second half)
        mid_point = len(assessments) // 2
        if mid_point > 0:
            first_half_avg = sum((a.score / a.max_score * 100) for a in assessments[:mid_point]) / mid_point
            second_half_avg = sum((a.score / a.max_score * 100) for a in assessments[mid_point:]) / (len(assessments) - mid_point)
            
            if second_half_avg > first_half_avg + 5:
                trend = "improving"
            elif second_half_avg < first_half_avg - 5:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = "insufficient_data"
        
        return {
            "student_id": student_id,
            "period_days": days,
            "assessments_count": len(assessments),
            "average_score": round(average_score, 2),
            "trend": trend,
            "latest_assessment_date": assessments[-1].assessment_date if assessments else None
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error calculating performance trend: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to calculate performance trend"
        )


@router.get("/high-risk-students")
def get_high_risk_students(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get list of high-risk students based on latest analytics"""
    try:
        # Get latest analytics for each student
        subquery = db.query(
            StudentAnalytics.student_id,
            func.max(StudentAnalytics.analysis_date).label('max_date')
        ).group_by(StudentAnalytics.student_id).subquery()
        
        high_risk_analytics = db.query(StudentAnalytics, Student).join(
            subquery,
            (StudentAnalytics.student_id == subquery.c.student_id) &
            (StudentAnalytics.analysis_date == subquery.c.max_date)
        ).join(Student).filter(
            StudentAnalytics.risk_level == "high"
        ).limit(limit).all()
        
        results = []
        for analytics, student in high_risk_analytics:
            results.append({
                "student_id": student.id,
                "student_name": f"{student.first_name} {student.last_name}",
                "email": student.email,
                "grade_level": student.grade_level,
                "risk_level": analytics.risk_level,
                "predicted_performance": analytics.predicted_performance,
                "engagement_score": analytics.engagement_score,
                "recommendation": analytics.recommendation,
                "analysis_date": analytics.analysis_date
            })
        
        return {
            "high_risk_count": len(results),
            "students": results
        }
    except Exception as e:
        logger.error(f"Error fetching high-risk students: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch high-risk students"
        )
