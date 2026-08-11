import pytest
from pydantic import ValidationError

from backend.app.schemas.course import CourseCreate

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