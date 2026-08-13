import pytest

from backend.app.models.course import Course
from backend.app.models.user import User, UserRole
from backend.app.repositories.lesson_repository import LessonRepository
from backend.app.repositories.course_repository import CourseRepository
from backend.app.schemas.lesson import LessonCreate
from backend.app.services.lesson_service import LessonService

def test_create_lesson(db_session):
    teacher = User(
        email='lesson_teacher@test.com',
        full_name='Lesson Teacher',
        hashed_password='test-password-hash',
        role=UserRole.TEACHER
    )

    db_session.add(teacher)
    db_session.commit()
    db_session.refresh(teacher)

    course_repository = CourseRepository(db_session)
    lesson_repository = LessonRepository(db_session)

    lesson_service = LessonService(lesson_repository=lesson_repository, course_repository=course_repository)

    course = course_repository.create(Course(title='Python Course', description='Learn Python.', teacher_id=teacher.id))
    lesson = lesson_service.create_lesson(course_id=course.id, lesson_data=LessonCreate(title='Variables', content='Variables store values.'))

    assert lesson.id is not None
    assert lesson.title == 'Variables'
    assert lesson.course_id == course.id


def test_create_lesson_fails_for_missing_course(db_session):
    course_repository = CourseRepository(db_session)
    lesson_repository = LessonRepository(db_session)

    service = LessonService(lesson_repository=lesson_repository, course_repository=course_repository)

    with pytest.raises(ValueError, match='Course not found'):
        service.create_lesson(course_id=999999, lesson_data=LessonCreate(title='Invalid lesson', content='This should fail.'))


def test_get_lesson(db_session):
    teacher = User(
        email='lesson_teacher2@test.com',
        full_name='Lesson Teacher',
        hashed_password='test-password-hash',
        role=UserRole.TEACHER
    )

    db_session.add(teacher)
    db_session.commit()
    db_session.refresh(teacher)

    course_repository = CourseRepository(db_session)
    lesson_repository = LessonRepository(db_session)

    course = course_repository.create(Course(title='FastAPI Course', description='Learn FastAPI.', teacher_id=teacher.id))

    service = LessonService(lesson_repository=lesson_repository, course_repository=course_repository)

    created_lesson = service.create_lesson(course_id=course.id, lesson_data=LessonCreate(title='Routing', content='FastAPI routing basics.'))

    found_lesson = service.get_lesson(created_lesson.id)

    assert found_lesson.id == created_lesson.id
    assert found_lesson.title == 'Routing'


def test_get_lesson_fails_when_missing(db_session):
    course_repository = CourseRepository(db_session)
    lesson_repository = LessonRepository(db_session)

    service = LessonService(lesson_repository=lesson_repository, course_repository=course_repository)

    with pytest.raises(ValueError, match='Lesson not found'):
        service.get_lesson(999999)

def test_list_course_lessons(db_session):

    teacher = User(
        email='lesson_teacher3@test.com',
        full_name='Lesson Teacher',
        hashed_password='test-password-hash',
        role=UserRole.TEACHER
    )

    db_session.add(teacher)
    db_session.commit()
    db_session.refresh(teacher)

    course_repository = CourseRepository(db_session)
    lesson_repository = LessonRepository(db_session)

    course = course_repository.create(Course(title='Python Course', description='Learn Python.', teacher_id=teacher.id))

    service = LessonService(lesson_repository=lesson_repository, course_repository=course_repository)

    service.create_lesson(course_id=course.id, lesson_data=LessonCreate(title='Lesson One', content='Lesson One.'))
    service.create_lesson(course_id=course.id, lesson_data=LessonCreate(title='Lesson Two', content='Lesson Two.'))

    lessons = service.list_course_lessons(course_id=course.id)

    assert len(lessons) == 2
    assert lessons[0].title == 'Lesson One'
    assert lessons[1].title == 'Lesson Two'