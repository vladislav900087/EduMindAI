# EduMindAI

EduMindAI is an online learning platform for teachers and students. Teachers create and sell courses, lessons, quizzes, and assignments; students enroll or purchase courses, learn materials, complete tasks and track their progress.

## Main Features

1. JWT authentication and role-based access: student, teacher, and administrator.
2. Course creation, publishing, enrollment, and lesson progress tracking.
3. Quizzes, attempts, scoring, and AI-assisted quiz-question generation.
4. Assignments, submissions, grading, email notifications, and deadline reminders.
5. Mock wallet, course purchases, teacher earnings, and immutable transaction history.
6. Docker compose deployment with FastAPI, PostgreSQL, Redis, Celery worker, Celery Beat, and React.

## Technology Stack

1. Backend: FastAPI, Python
2. Database: PostgreSQL
3. ORM: SQLAlchemy
4. Migrations: Alembic
5. Background tasks: Celery, Redis
6. Frontend: React, TypeScript, Vite, Tailwind CSS
7. AI: Google Gemini API
8. Tests: Pytest
9. Deployment: Docker, Docker compose, Nginx


## Dashboard:
![Screenshot 2026-10-27 at 00.21.44.png](screenshots/Screenshot%202026-10-27%20at%2000.21.44.png)
## Teacher's Course Creation Page
![Screenshot 2026-10-27 at 00.22.01.png](screenshots/Screenshot%202026-10-27%20at%2000.22.01.png)
## Teacher's Course Page:
![Screenshot 2026-10-27 at 00.22.41.png](screenshots/Screenshot%202026-10-27%20at%2000.22.41.png)
## AI-assisted Quiz Generation Page:
![Screenshot 2026-10-27 at 00.58.35.png](screenshots/Screenshot%202026-10-27%20at%2000.58.35.png)
![Screenshot 2026-10-27 at 00.58.56.png](screenshots/Screenshot%202026-10-27%20at%2000.58.56.png)
![Screenshot 2026-10-27 at 00.59.27.png](screenshots/Screenshot%202026-10-27%20at%2000.59.27.png)
## Payment-required Course Page (Role: Student):
![Screenshot 2026-10-27 at 14.38.43.png](screenshots/Screenshot%202026-10-27%20at%2014.38.43.png)
## Student's Course Progress Page:
![Screenshot 2026-10-27 at 14.38.56.png](screenshots/Screenshot%202026-10-27%20at%2014.38.56.png)
![Screenshot 2026-10-27 at 14.39.10.png](screenshots/Screenshot%202026-10-27%20at%2014.39.10.png)
## Quiz Page (Role: Student):
![Screenshot 2026-10-27 at 14.39.36.png](screenshots/Screenshot%202026-10-27%20at%2014.39.36.png)
![Screenshot 2026-10-27 at 14.40.49.png](screenshots/Screenshot%202026-10-27%20at%2014.40.49.png)
## Quiz History Page (Role: Student):
![Screenshot 2026-10-27 at 14.41.11.png](screenshots/Screenshot%202026-10-27%20at%2014.41.11.png)
## Assignment Submission Page (Role: Student):
![Screenshot 2026-10-27 at 14.41.55.png](screenshots/Screenshot%202026-10-27%20at%2014.41.55.png)
![Screenshot 2026-10-27 at 14.42.08.png](screenshots/Screenshot%202026-10-27%20at%2014.42.08.png)
## Teacher Earnings Page:
![Screenshot 2026-10-27 at 14.43.03.png](screenshots/Screenshot%202026-10-27%20at%2014.43.03.png)
## Teacher Grading Student's Assignment Page:
![Screenshot 2026-10-27 at 14.43.52.png](screenshots/Screenshot%202026-10-27%20at%2014.43.52.png)
![Screenshot 2026-10-27 at 14.44.14.png](screenshots/Screenshot%202026-10-27%20at%2014.44.14.png)

## Run With Docker

1. Copy 'env.example' to 'env'.
2. Fill in secure values for database credentials, 'SECRET KEY', SMTP settings and 'GEMINI_API_KEY'.
3. Start the application:


```bash
docker compose up -d --build


