import pytest

from backend.app.models.user import User, UserRole
from backend.app.models.course import CourseStatus
from backend.app.repositories.course_repository import CourseRepository
from backend.app.schemas.course import CourseCreate
from backend.app.services.course_service import CourseService


def test_create_course(db_session):
    teacher = User(
        email='service_teacher@test.com',
        full_name='Service Teacher',
        hashed_password='test-password-hash',
        role=UserRole.TEACHER
    )

    db_session.add(teacher)
    db_session.commit()
    db_session.refresh(teacher)

    repository = CourseRepository(db_session)
    service = CourseService(repository)

    course_data = CourseCreate(title='Python for beginners', description='Learn Python step-by-step.')

    course = service.create_course(course_data, teacher)

    assert course.id is not None
    assert course.title == 'Python for beginners'
    assert course.description == 'Learn Python step-by-step.'
    assert course.teacher_id == teacher.id


def test_get_course(db_session):

    teacher = User(
        email='service_teacher2@test.com',
        full_name='Service Teacher',
        hashed_password='test-password-hash',
        role=UserRole.TEACHER
    )

    db_session.add(teacher)
    db_session.commit()
    db_session.refresh(teacher)

    repository = CourseRepository(db_session)
    service = CourseService(repository)

    course_data = CourseCreate(title='FastAPI for beginners', description='Learn FastAPI step-by-step.')

    created_course = service.create_course(course_data, teacher)

    found_course = service.get_course(created_course.id)

    assert found_course.id is not None
    assert found_course.title == 'FastAPI for beginners'
    assert found_course.description == 'Learn FastAPI step-by-step.'
    assert found_course.teacher_id == teacher.id

def test_list_courses(db_session):

    teacher = User(
        email='service_teacher3@test.com',
        full_name='Service Teacher',
        hashed_password='test-password-hash',
        role=UserRole.TEACHER
    )

    db_session.add(teacher)
    db_session.commit()
    db_session.refresh(teacher)



    repository = CourseRepository(db_session)
    service = CourseService(repository)

    course_1 = service.create_course(CourseCreate(title='English for beginners', description='Learn English step-by-step.'), teacher)
    course_2 = service.create_course(CourseCreate(title='German for beginners', description='Learn German step-by-step.'), teacher)



    courses = service.list_courses()

    assert len(courses) == 2
    assert course_1.title == 'English for beginners'
    assert course_2.title == 'German for beginners'


def test_list_courses_by_teacher(db_session):
    teacher = User(
        email='service_teacher4@test.com',
        full_name='Service Teacher',
        hashed_password='test-password-hash',
        role=UserRole.TEACHER
    )

    db_session.add(teacher)
    db_session.commit()
    db_session.refresh(teacher)

    repository = CourseRepository(db_session)
    service = CourseService(repository)

    course_1 = service.create_course(
        CourseCreate(title='Course One', description='Learn Course One step-by-step.'), teacher)
    course_2 = service.create_course(
        CourseCreate(title='Course Two', description='Learn Course Two step-by-step.'), teacher)

    courses = service.list_teacher_courses(teacher.id)

    assert len(courses) == 2
    assert course_1.title == 'Course One'
    assert course_2.title == 'Course Two'


def test_get_course_raises_when_course_does_not_exist(db_session):
    repository = CourseRepository(db_session)
    service = CourseService(repository)

    with pytest.raises(ValueError, match='Course not found'):
        service.get_course(999999)


def test_publish_course(db_session):
    teacher = User(email='test_publish_course_teacher@example.com', full_name='Service Teacher', hashed_password='test-password-hash', role=UserRole.TEACHER)
    db_session.add(teacher)
    db_session.commit()
    db_session.refresh(teacher)

    repository = CourseRepository(db_session)
    service = CourseService(repository)

    course = service.create_course(CourseCreate(title='A draft course', description='A course that is soon going to be published'), teacher)
    published_course = service.publish_course(course.id)

    assert published_course is not None
    assert published_course.status == CourseStatus.PUBLISHED


def test_publish_missing_course(db_session):

    repository = CourseRepository(db_session)
    service = CourseService(repository)

    with pytest.raises(ValueError, match='Course not found'):
        service.publish_course(999999)


def test_publish_already_published_course(db_session):
    teacher = User(email='test_publish_already_published_course_teacher@example.com', full_name='Service Teacher', role=UserRole.TEACHER, hashed_password='test-password-hash')

    db_session.add(teacher)
    db_session.commit()
    db_session.refresh(teacher)

    repository = CourseRepository(db_session)
    service = CourseService(repository)

    course = service.create_course(CourseCreate(title='Some course', description='Some course description'), teacher)

    published_course = service.publish_course(course.id)

    assert published_course is not None
    assert published_course.status == CourseStatus.PUBLISHED

    with pytest.raises(ValueError, match='Only draft courses can be published'):
        service.publish_course(published_course.id)


def test_publish_archived_course(db_session):
    teacher = User(email='test_publish_archived_course_teacher@example.com', full_name='Service Teacher', role=UserRole.TEACHER, hashed_password='test-password-hash')

    db_session.add(teacher)
    db_session.commit()
    db_session.refresh(teacher)

    repository = CourseRepository(db_session)
    service = CourseService(repository)

    course = service.create_course(CourseCreate(title='Archived course', description='Archived course cannot be published.'), teacher)

    course.status = CourseStatus.ARCHIVED

    updated_course = repository.update(course)

    with pytest.raises(ValueError, match='Only draft courses can be published'):
        service.publish_course(updated_course.id)
