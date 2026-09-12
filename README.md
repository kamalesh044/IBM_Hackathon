# Education Analytics Platform

A predictive learning analytics platform that transforms education from reactive crisis management to proactive, personalized support for K-12 and higher education institutions.

## Product Vision

To make learning analytics predictive, transparent, and actionable for every educator, enabling them to support student success through data-driven insights.

## Target Audience

- **K-12 Classroom Teachers**: Need actionable insights to identify at-risk students early
- **Higher Education Instructors**: Require tools to personalize learning at scale
- **Academic Administrators**: Need data to optimize educational strategies and resource allocation

## Core Features

- **Student Management**: Complete CRUD operations for student records
- **Assessment Tracking**: Record and monitor student assessments across subjects
- **Predictive Analytics**: Risk assessment and performance predictions
- **Performance Trends**: Track student progress over time
- **Risk Identification**: Identify high-risk students requiring intervention

## Technology Stack

- **Backend Framework**: FastAPI (Python)
- **Database**: SQLAlchemy ORM (SQLite for development, PostgreSQL/MySQL for production)
- **API**: RESTful API with automatic OpenAPI documentation
- **Validation**: Pydantic for data validation
- **Architecture**: Modular Monolith with clear separation of concerns

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Virtual environment tool (venv or virtualenv)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd education-analytics-platform
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` file and update the following variables:
- `SECRET_KEY`: Generate a strong random string for production
- `DATABASE_URL`: Configure your database connection (default is SQLite)
- `ALLOWED_ORIGINS`: Add your frontend URLs for CORS

## Running the Application

### Development Server

```bash
# From the project root directory
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

### Production Server

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### Health Check
- `GET /` - Basic health check
- `GET /health` - Detailed health status

### Students
- `POST /api/v1/students` - Create a new student
- `GET /api/v1/students` - List all students (with pagination and filters)
- `GET /api/v1/students/{student_id}` - Get specific student
- `PUT /api/v1/students/{student_id}` - Update student information
- `DELETE /api/v1/students/{student_id}` - Delete student

### Assessments
- `POST /api/v1/students/{student_id}/assessments` - Create assessment for student
- `GET /api/v1/students/{student_id}/assessments` - Get student's assessments

### Analytics
- `POST /api/v1/analytics` - Create analytics record
- `GET /api/v1/analytics/student/{student_id}` - Get student analytics history
- `GET /api/v1/analytics/student/{student_id}/latest` - Get latest analytics
- `GET /api/v1/analytics/risk-summary` - Get risk distribution summary
- `GET /api/v1/analytics/student/{student_id}/performance-trend` - Get performance trend
- `GET /api/v1/analytics/high-risk-students` - Get list of high-risk students

## Database Schema

### Students Table
- Student identification and contact information
- Enrollment and activity status
- Grade level tracking

### Assessments Table
- Assessment records with scores
- Subject and assessment type tracking
- Temporal tracking of student performance

### Student Analytics Table
- Risk level assessment (low, medium, high)
- Predicted performance metrics
- Engagement and attendance scores
- Personalized recommendations

## Project Structure

```
education-analytics-platform/
├── backend/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration management
│   ├── database.py          # Database connection and session
│   ├── models.py            # SQLAlchemy database models
│   ├── schemas.py           # Pydantic validation schemas
│   └── routers/             # API route handlers
│       ├── __init__.py
│       ├── students.py      # Student and assessment endpoints
│       └── analytics.py     # Analytics endpoints
├── .env.example             # Environment variables template
├── README.md                # This file
└── requirements.txt         # Python dependencies
```

## Development Guidelines

### Adding New Features

1. **Models**: Add database models in `backend/models.py`
2. **Schemas**: Define Pydantic schemas in `backend/schemas.py`
3. **Routes**: Create route handlers in `backend/routers/`
4. **Register**: Include router in `backend/main.py`

### Code Quality

- Follow PEP 8 style guidelines
- Add type hints to function signatures
- Include docstrings for functions and classes
- Implement proper error handling
- Add logging for important operations

### Security Best Practices

- Never commit `.env` file with secrets
- Use environment variables for sensitive data
- Implement input validation using Pydantic
- Use parameterized queries (SQLAlchemy ORM)
- Enable CORS only for trusted origins
- Use HTTPS in production

## Testing

Run the application and test endpoints using the interactive API documentation at http://localhost:8000/docs

Example workflow:
1. Create a student using POST /api/v1/students
2. Add assessments using POST /api/v1/students/{student_id}/assessments
3. Create analytics using POST /api/v1/analytics
4. View risk summary using GET /api/v1/analytics/risk-summary

## Deployment

### Database Migration (Production)

For production, use PostgreSQL or MySQL:

1. Update `DATABASE_URL` in `.env`:
```
DATABASE_URL=postgresql://user:password@localhost:5432/education_analytics
```

2. Install database driver:
```bash
# For PostgreSQL
pip install psycopg2-binary

# For MySQL
pip install pymysql
```

### Environment Configuration

Ensure these environment variables are set in production:
- `DEBUG=False`
- Strong `SECRET_KEY`
- Production database URL
- Appropriate `ALLOWED_ORIGINS`
- `LOG_LEVEL=WARNING` or `ERROR`

## Troubleshooting

### Database Connection Issues
- Verify `DATABASE_URL` in `.env`
- Ensure database server is running
- Check database credentials

### CORS Errors
- Add frontend URL to `ALLOWED_ORIGINS` in `.env`
- Restart the server after configuration changes

### Import Errors
- Ensure virtual environment is activated
- Verify all dependencies are installed: `pip install -r backend/requirements.txt`

## Support

For issues and questions:
1. Check the API documentation at `/docs`
2. Review error logs for detailed information
3. Verify environment configuration

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]
