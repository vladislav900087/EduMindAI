import pytest

from backend.app.models.course import Course
from backend.app.models.user import User, UserRole
from backend.app.repositories.course_enrollment_repository import CourseEnrollmentRepository
from backend.app.repositories.course_repository import CourseRepository
from backend.app.services.course_enrollment_service import CourseEnrollmentService


def test_enroll_student(db_session):
    teacher = User(
        email='enrollment_teacher@test.com',
        full_name='Enrollment Teacher',
        hashed_password='test-password-hash',
        role=UserRole.TEACHER
    )

    student = User(
        email='enrollment_student@test.com',
        full_name='Enrollment Student',
        hashed_password='test-password-hash',
        role=UserRole.STUDENT
    )

    db_session.add_all([teacher, student])
    db_session.commit()

    db_session.refresh(teacher)
    db_session.refresh(student)

    course_repository = CourseRepository(db=db_session)
    enrollment_repository = CourseEnrollmentRepository(db=db_session)

    course = course_repository.create(Course(title='Python course', description='Learn Python.', teacher_id=teacher.id))
    service = CourseEnrollmentService(enrollment_repository=enrollment_repository, course_repository=course_repository)

    enrollment = service.enroll(student_id=student.id, course_id=course.id)

    assert enrollment is not None
    assert enrollment.student_id == student.id
    assert enrollment.course_id == course.id

def test_enroll_fails_when_course_does_not_exist(db_session):
    student = User(
        email='missing_course_student@test.com',
        full_name='Missing Course Student',
        hashed_password='test-password-hash',
        role=UserRole.STUDENT
    )

    db_session.add(student)
    db_session.commit()
    db_session.refresh(student)

    course_repository = CourseRepository(db=db_session)
    enrollment_repository = CourseEnrollmentRepository(db=db_session)

    service = CourseEnrollmentService(enrollment_repository=enrollment_repository, course_repository=course_repository)

    with pytest.raises(ValueError, match='Course not found'):
        service.enroll(student_id=student.id, course_id=999999)


def test_duplicate_enrollment_is_rejected(db_session):
    teacher = User(
        email='duplicate_teacher@test.com',
        full_name='Duplicate Teacher',
        hashed_password='test-password-hash',
        role=UserRole.TEACHER
    )

    student = User(
        email='duplicate_student@test.com',
        full_name='Duplicate Student',
        hashed_password='test-password-hash',
        role=UserRole.STUDENT
    )

    db_session.add_all([teacher, student])
    db_session.commit()
    db_session.refresh(teacher)
    db_session.refresh(student)

    course_repository = CourseRepository(db=db_session)
    enrollment_repository = CourseEnrollmentRepository(db=db_session)

    course = course_repository.create(Course(title='Duplicate Test Course', description='Test duplicate enrollment', teacher_id=teacher.id))

    service = CourseEnrollmentService(enrollment_repository=enrollment_repository, course_repository=course_repository)

    service.enroll(student_id=student.id, course_id=course.id)

    with pytest.raises(ValueError, match='Student is already enrolled'):
        service.enroll(student_id=student.id, course_id=course.id)

def test_list_student_enrollments(db_session):
    teacher = User(
        email='list_teacher@test.com',
        full_name='List Teacher',
        hashed_password='test-password-hash',
        role=UserRole.TEACHER
    )

    student = User(
        email='list_student@test.com',
        full_name='List Student',
        hashed_password='test-password-hash',
        role=UserRole.STUDENT
    )

    db_session.add_all([teacher, student])
    db_session.commit()
    db_session.refresh(teacher)
    db_session.refresh(student)

    course_repository = CourseRepository(db=db_session)
    enrollment_repository = CourseEnrollmentRepository(db=db_session)

    course_one = course_repository.create(Course(title='List Test Course One', description='Test list student enrollments', teacher_id=teacher.id))
    course_two = course_repository.create(Course(title='List Test Course Two', description='Test list student enrollments', teacher_id=teacher.id))

    service = CourseEnrollmentService(enrollment_repository=enrollment_repository, course_repository=course_repository)

    service.enroll(student_id=student.id, course_id=course_one.id)
    service.enroll(student_id=student.id, course_id=course_two.id)

    student_enrollments = service.list_student_enrollments(student_id=student.id)

    assert len(student_enrollments) == 2


def test_list_course_enrollments(db_session):
    teacher = User(
        email='course_list_teacher@test.com',
        full_name='Course List Teacher',
        hashed_password='test-password-hash',
        role=UserRole.TEACHER
    )

    student_one = User(
        email='course_list_student_one@test.com',
        full_name='Course List Student One',
        hashed_password='test-password-hash',
        role=UserRole.STUDENT
    )

    student_two = User(
        email='course_list_student_two@test.com',
        full_name='Course List Student Two',
        hashed_password='test-password-hash',
        role=UserRole.STUDENT
    )

    db_session.add_all([teacher, student_one, student_two])
    db_session.commit()
    db_session.refresh(teacher)
    db_session.refresh(student_one)
    db_session.refresh(student_two)

    course_repository = CourseRepository(db=db_session)
    enrollment_repository = CourseEnrollmentRepository(db=db_session)

    course = course_repository.create(Course(title='Course List', description='Course list enrollments test', teacher_id=teacher.id))

    service = CourseEnrollmentService(enrollment_repository=enrollment_repository, course_repository=course_repository)

    service.enroll(student_id=student_one.id, course_id=course.id)
    service.enroll(student_id=student_two.id, course_id=course.id)

    course_enrollments = service.list_course_enrollments(course_id=course.id)

    assert len(course_enrollments) == 2


def test_unenroll_student(db_session):
    teacher = User(
        email='unenroll_teacher@test.com',
        full_name='Unenroll Teacher',
        hashed_password='test-password-hash',
        role=UserRole.TEACHER
    )

    student = User(
        email='unenroll_student@test.com',
        full_name='Unenroll Student',
        hashed_password='test-password-hash',
        role=UserRole.STUDENT
    )

    db_session.add_all([teacher, student])
    db_session.commit()
    db_session.refresh(teacher)
    db_session.refresh(student)

    course_repository = CourseRepository(db=db_session)
    enrollment_repository = CourseEnrollmentRepository(db=db_session)

    course = course_repository.create(Course(title='Unenroll student test', description='Student unenrollment test', teacher_id=teacher.id))
    service = CourseEnrollmentService(enrollment_repository=enrollment_repository, course_repository=course_repository)
    # student enrollment
    service.enroll(student_id=student.id, course_id=course.id)

    student_enrollments = service.list_student_enrollments(student_id=student.id)
    course_enrollments = service.list_course_enrollments(course_id=course.id)
    current_enrollment = enrollment_repository.get_by_student_and_course(student_id=student.id, course_id=course.id)
    # test student and course enrollments
    assert len(student_enrollments) == 1
    assert len(course_enrollments) == 1
    assert current_enrollment == student_enrollments[0]

    # student unenrollment
    service.unenroll(student_id=student.id, course_id=course.id)

    student_enrollments = service.list_student_enrollments(student_id=student.id)
    course_enrollments = service.list_course_enrollments(course_id=course.id)
    current_enrollment = enrollment_repository.get_by_student_and_course(student_id=student.id, course_id=course.id)

    # test whether student has unenrolled from the course
    assert len(student_enrollments) == 0
    assert len(course_enrollments) == 0
    assert current_enrollment is None

def test_unenroll_fails_when_enrollment_does_not_exist(db_session):
    teacher = User(
        email='missing_enrollment_teacher@test.com',
        full_name='Missing Enrollment Teacher',
        hashed_password='test-password-hash',
        role=UserRole.TEACHER
    )

    student = User(
        email='missing_enrollment_student@test.com',
        full_name='Missing Enrollment Student',
        hashed_password='test-password-hash',
        role=UserRole.STUDENT
    )

    db_session.add_all([teacher, student])
    db_session.commit()
    db_session.refresh(teacher)
    db_session.refresh(student)

    course_repository = CourseRepository(db=db_session)
    enrollment_repository = CourseEnrollmentRepository(db=db_session)

    course = course_repository.create(Course(title='Missing Enrollment Test', description='Course missing enrollment test', teacher_id=teacher.id))

    service = CourseEnrollmentService(enrollment_repository=enrollment_repository, course_repository=course_repository)

    with pytest.raises(ValueError, match='Enrollment not found'):
        service.unenroll(student_id=student.id, course_id=course.id)

