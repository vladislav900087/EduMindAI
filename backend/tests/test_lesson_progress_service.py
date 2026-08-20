import pytest

from backend.app.repositories.course_enrollment_repository import CourseEnrollmentRepository
from backend.app.services.course_enrollment_service import CourseEnrollmentService
from backend.app.repositories.course_repository import CourseRepository
from backend.app.services.course_service import CourseService
from backend.app.repositories.lesson_progress_repository import LessonProgressRepository
from backend.app.repositories.lesson_repository import LessonRepository
from backend.app.services.lesson_progress_service import LessonProgressService
from backend.app.models.user import User, UserRole
from backend.app.models.course import Course, CourseStatus
from backend.app.models.lesson import Lesson
from backend.app.models.lesson_progress import LessonProgress
from backend.app.core.security import hash_password


def create_test_user(db_session, email: str, role: UserRole) -> User:
    user = User(email=email, hashed_password=hash_password('SuperSecurePassword123!'), role=role, full_name='Test User')

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


def test_student_can_mark_lesson_complete(db_session):
    teacher = create_test_user(db_session, 'test_student_can_mark_lesson_complete_test_teacher@example.com', role=UserRole.TEACHER)
    student = create_test_user(db_session, 'this_student_can_mark_lesson_complete@example.com', role=UserRole.STUDENT)

    course_repository = CourseRepository(db_session)
    course_service = CourseService(course_repository)
    enrollment_repository = CourseEnrollmentRepository(db_session)
    enrollment_service = CourseEnrollmentService(enrollment_repository=enrollment_repository, course_repository=course_repository)
    lesson_repository = LessonRepository(db_session)
    lesson_progress_repository = LessonProgressRepository(db_session)
    lesson_progress_service = LessonProgressService(progress_repository=lesson_progress_repository, enrollment_repository=enrollment_repository, lesson_repository=lesson_repository, course_repository=course_repository)

    course = course_repository.create(Course(title='Any Course', description='An Description', teacher_id=teacher.id))
    published_course = course_service.publish_course(course.id)
    lesson = lesson_repository.create(Lesson(title='Any Lesson', content='Any Content', course_id=published_course.id))
    student_course_enrollment = enrollment_service.enroll(student_id=student.id, course_id=published_course.id)

    assert student_course_enrollment is not None

    lesson_marked_complete = lesson_progress_service.mark_lesson_complete(student_id=student.id, lesson_id=lesson.id)

    assert lesson_marked_complete is not None
    assert lesson_marked_complete.lesson_id == lesson.id
    assert lesson_marked_complete.student_id == student.id


def test_cannot_complete_missing_lesson(db_session):
    student = create_test_user(db_session, 'this_student_cannot_complete_missing_lesson@example.com', role=UserRole.STUDENT)


    course_repository = CourseRepository(db_session)
    enrollment_repository = CourseEnrollmentRepository(db_session)
    lesson_repository = LessonRepository(db_session)
    lesson_progress_repository = LessonProgressRepository(db_session)


    lesson_progress_service = LessonProgressService(progress_repository=lesson_progress_repository, enrollment_repository=enrollment_repository, lesson_repository=lesson_repository, course_repository=course_repository)

    with pytest.raises(ValueError, match='Lesson not found'):
        lesson_progress_service.mark_lesson_complete(student_id=student.id, lesson_id=999999)

def test_student_cannot_complete_lesson_without_enrollment(db_session):
    teacher = create_test_user(db_session, email='test_student_cannot_complete_lesson_without_enrollment_test_teacher@example.com', role=UserRole.TEACHER)
    student = create_test_user(db_session, email='this_student_cannot_complete_lesson_without_enrollment@example.com', role=UserRole.STUDENT)

    course_repository = CourseRepository(db_session)
    course_service = CourseService(course_repository)
    enrollment_repository = CourseEnrollmentRepository(db_session)
    lesson_repository = LessonRepository(db_session)
    lesson_progress_repository = LessonProgressRepository(db_session)


    lesson_progress_service = LessonProgressService(enrollment_repository=enrollment_repository, lesson_repository=lesson_repository, progress_repository=lesson_progress_repository, course_repository=course_repository)

    course = course_repository.create(Course(title='Course without enrollment', description='Unfortunately, nobody likes this course and wants to enroll to it', teacher_id=teacher.id))
    published_course = course_service.publish_course(course_id=course.id)
    lesson = lesson_repository.create(Lesson(title='A lesson of enrollmentless course', content='A content', course_id=published_course.id))

    with pytest.raises(ValueError, match='Student is not enrolled in this course'):
        lesson_progress_service.mark_lesson_complete(student_id=student.id, lesson_id=lesson.id)


def test_student_cannot_complete_lesson_twice(db_session):
    teacher = create_test_user(db_session, email='test_student_cannot_complete_lesson_twice_test_teacher@example.com', role=UserRole.TEACHER)
    student = create_test_user(db_session, email='this_student_cannot_complete_lesson_twice@example.com', role=UserRole.STUDENT)

    course_repository = CourseRepository(db_session)
    course_service = CourseService(course_repository)
    enrollment_repository = CourseEnrollmentRepository(db_session)
    lesson_repository = LessonRepository(db_session)
    lesson_progress_repository = LessonProgressRepository(db_session)
    lesson_progress_service = LessonProgressService(enrollment_repository=enrollment_repository, lesson_repository=lesson_repository, progress_repository=lesson_progress_repository, course_repository=course_repository)
    enrollment_service = CourseEnrollmentService(enrollment_repository=enrollment_repository, course_repository=course_repository)

    course = course_repository.create(Course(title='Course with enrollment', description='A description', teacher_id=teacher.id))
    assert course.status == CourseStatus.DRAFT
    published_course = course_service.publish_course(course_id=course.id)
    assert published_course.status == CourseStatus.PUBLISHED

    lesson = lesson_repository.create(Lesson(title='Good Lesson!', content='Good Content!', course_id=published_course.id))
    student_course_enrollment = enrollment_service.enroll(student_id=student.id, course_id=course.id)

    assert student_course_enrollment.student_id == student.id
    assert student_course_enrollment.course_id == course.id

    lesson_marked_complete = lesson_progress_service.mark_lesson_complete(student_id=student.id, lesson_id=lesson.id)

    assert lesson_marked_complete is not None
    assert lesson_marked_complete.student_id == student.id
    assert lesson_marked_complete.lesson_id == lesson.id

    with pytest.raises(ValueError, match='Lesson is already completed'):
        lesson_progress_service.mark_lesson_complete(student_id=student.id, lesson_id=lesson.id)




def test_get_course_progress(db_session):
    teacher = create_test_user(db_session, email='test_get_course_progress_test_teacher@example.com', role=UserRole.TEACHER)
    student = create_test_user(db_session, email='this_student_can_get_his_own_course_progress@example.com', role=UserRole.STUDENT)

    course_repository = CourseRepository(db_session)
    course_service = CourseService(course_repository)
    enrollment_repository = CourseEnrollmentRepository(db_session)
    enrollment_service = CourseEnrollmentService(enrollment_repository=enrollment_repository, course_repository=course_repository)
    lesson_repository = LessonRepository(db_session)
    lesson_progress_repository = LessonProgressRepository(db_session)
    lesson_progress_service = LessonProgressService(enrollment_repository=enrollment_repository, lesson_repository=lesson_repository, progress_repository=lesson_progress_repository, course_repository=course_repository)

    course = course_repository.create(Course(title='A Course', description='A description', teacher_id=teacher.id))
    assert course.status == CourseStatus.DRAFT

    published_course = course_service.publish_course(course_id=course.id)
    assert published_course.status == CourseStatus.PUBLISHED

    lesson_one = lesson_repository.create(Lesson(title='Lesson One', content='The content of Lesson One', course_id=published_course.id))
    lesson_two = lesson_repository.create(Lesson(title='Lesson Two', content='The content of Lesson Two', course_id=published_course.id))
    lesson_three = lesson_repository.create(Lesson(title='Lesson Three', content='The content of Lesson Three', course_id=published_course.id))
    lesson_four = lesson_repository.create(Lesson(title='Lesson Four', content='The content of Lesson Four', course_id=published_course.id))

    assert lesson_one.course_id == published_course.id
    assert lesson_two.course_id == published_course.id
    assert lesson_three.course_id == published_course.id
    assert lesson_four.course_id == published_course.id

    student_course_enrollment = enrollment_service.enroll(student_id=student.id, course_id=course.id)

    assert student_course_enrollment.student_id == student.id
    assert student_course_enrollment.course_id == course.id

    lesson_one_marked_complete = lesson_progress_service.mark_lesson_complete(student_id=student.id, lesson_id=lesson_one.id)
    lesson_two_marked_complete = lesson_progress_service.mark_lesson_complete(student_id=student.id, lesson_id=lesson_two.id)

    assert lesson_one_marked_complete is not None
    assert lesson_one_marked_complete.student_id == student.id
    assert lesson_one_marked_complete.lesson_id == lesson_one.id

    assert lesson_two_marked_complete is not None
    assert lesson_two_marked_complete.student_id == student.id
    assert lesson_two_marked_complete.lesson_id == lesson_two.id

    student_course_progress = lesson_progress_service.get_course_progress(student_id=student.id, course_id=course.id)

    assert student_course_progress is not None
    assert student_course_progress['course_id'] == course.id
    assert student_course_progress['total_lessons'] == 4
    assert student_course_progress['completed_lessons'] == 2
    assert student_course_progress['progress_percentage'] == 50.0

def test_get_course_progress_for_course_with_no_lessons(db_session):

    teacher = create_test_user(db_session, 'test_get_course_progress_for_course_with_no_lessons_test_teacher@example.com', role=UserRole.TEACHER)
    student = create_test_user(db_session, 'this_student_tries_getting_course_progress_for_course_with_no_lessons@example.com', role=UserRole.STUDENT)

    course_repository = CourseRepository(db_session)
    course_service = CourseService(course_repository)
    enrollment_repository = CourseEnrollmentRepository(db_session)
    enrollment_service = CourseEnrollmentService(enrollment_repository, course_repository)
    lesson_repository = LessonRepository(db_session)
    lesson_progress_repository = LessonProgressRepository(db_session)
    lesson_progress_service = LessonProgressService(progress_repository=lesson_progress_repository, enrollment_repository=enrollment_repository, course_repository=course_repository, lesson_repository=lesson_repository)

    course = course_repository.create(Course(title='A course with no lessons', description='A description of the lessonless course', teacher_id=teacher.id))
    assert course.status == CourseStatus.DRAFT
    published_course = course_service.publish_course(course_id=course.id)
    assert published_course.status == CourseStatus.PUBLISHED

    student_course_enrollment = enrollment_service.enroll(student_id=student.id, course_id=course.id)
    assert student_course_enrollment.student_id == student.id
    assert student_course_enrollment.course_id == course.id

    student_course_progress = lesson_progress_service.get_course_progress(student_id=student.id, course_id=course.id)

    assert student_course_progress is not None
    assert student_course_progress['course_id'] == course.id
    assert student_course_progress['total_lessons'] == 0
    assert student_course_progress['completed_lessons'] == 0
    assert student_course_progress['progress_percentage'] == 0.0


def test_student_cannot_get_progress_for_unenrolled_course(db_session):
    teacher = create_test_user(db_session, 'test_student_cannot_get_progress_for_unenrolled_course_test_teacher@example.com', role=UserRole.TEACHER)
    student = create_test_user(db_session, 'this_student_cannot_get_course_progress_for_unenrolled_course@example.com', role=UserRole.STUDENT)

    course_repository = CourseRepository(db_session)
    course_service = CourseService(course_repository)

    enrollment_repository = CourseEnrollmentRepository(db_session)


    lesson_repository = LessonRepository(db_session)
    lesson_progress_repository = LessonProgressRepository(db_session)
    lesson_progress_service = LessonProgressService(progress_repository=lesson_progress_repository, enrollment_repository=enrollment_repository, course_repository=course_repository, lesson_repository=lesson_repository)

    course = course_repository.create(Course(title='An unenrolled course', description='The description of the unenrolled course', teacher_id=teacher.id))
    assert course.status == CourseStatus.DRAFT

    published_course = course_service.publish_course(course_id=course.id)
    assert published_course.status == CourseStatus.PUBLISHED

    with pytest.raises(ValueError, match='Student is not enrolled in this course'):
        student_course_progress = lesson_progress_service.get_course_progress(student_id=student.id, course_id=course.id)


def test_get_course_progress_for_missing_course(db_session):
    student = create_test_user(db_session, email='this_student_cannot_get_progress_for_missing_course@example.com', role=UserRole.STUDENT)

    course_repository = CourseRepository(db_session)
    enrollment_repository = CourseEnrollmentRepository(db_session)
    lesson_repository = LessonRepository(db_session)
    lesson_progress_repository = LessonProgressRepository(db_session)
    lesson_progress_service = LessonProgressService(enrollment_repository=enrollment_repository, course_repository=course_repository, lesson_repository=lesson_repository, progress_repository=lesson_progress_repository)

    with pytest.raises(ValueError, match='Course not found'):
        lesson_progress_service.get_course_progress(student_id=student.id, course_id=999999)






























