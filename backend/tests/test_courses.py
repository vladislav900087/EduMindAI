import pytest
from pydantic import ValidationError


from backend.app.schemas.course import CourseCreate
from backend.app.models.course import Course
from backend.app.repositories.course_repository import CourseRepository
from backend.app.models.user import User, UserRole

def test_course_create_accepts_valid_data():
    course = CourseCreate(
        title='Introduction to Python',
        description='A beginner Python course'
    )

    assert course.title == 'Introduction to Python'
    assert course.description == 'A beginner Python course'


def test_course_create_rejects_empty_title():
    with pytest.raises(ValidationError):
        CourseCreate(title='', description='A course.')


def test_course_create_rejects_title_over_200_characters():
    with pytest.raises(ValidationError):
        CourseCreate(
            title='A' * 201,
            description='A course.'
        )


def test_create_course(db_session):
    teacher = User(
        email='teacher@test.com',
        full_name='Test Teacher',
        hashed_password='test-password-hash',
        role=UserRole.TEACHER
    )
    db_session.add(teacher)
    db_session.commit()
    db_session.refresh(teacher)

    repository = CourseRepository(db_session)

    course = Course(title='Python Basics', description='Learn Python from scratch.', teacher_id=teacher.id)

    created_course = repository.create(course)

    assert created_course.id is not None
    assert created_course.title == 'Python Basics'
    assert created_course.teacher_id == teacher.id


def test_get_course_by_id(db_session):
    teacher = User(
        email='teacher2@test.com',
        full_name='Test Teacher',
        hashed_password='test-password-hash',
        role=UserRole.TEACHER
    )

    db_session.add(teacher)
    db_session.commit()
    db_session.refresh(teacher)

    course = Course(title='FastAPI basics', description='Learn FastAPI from scratch.', teacher_id=teacher.id)

    repository = CourseRepository(db_session)
    created_course = repository.create(course)

    found_course = repository.get_by_id(created_course.id)

    assert found_course is not None
    assert found_course.id == created_course.id
    assert found_course.title == 'FastAPI basics'


def test_list_courses_by_teacher(db_session):
    teacher = User(
        email='teacher3@test.com',
        full_name='Test Teacher',
        hashed_password='test-password-hash',
        role=UserRole.TEACHER
    )

    db_session.add(teacher)
    db_session.commit()
    db_session.refresh(teacher)

    repository = CourseRepository(db_session)

    repository.create(Course(
        title='Course One',
        description='First course.',
        teacher_id=teacher.id
    ))

    repository.create(
        Course(title='Course Two', description='Second course.', teacher_id=teacher.id)
    )

    courses = repository.list_by_teacher(teacher.id)

    assert len(courses) == 2
    assert courses[0].title == 'Course Two'
    assert courses[1].title == 'Course One'



