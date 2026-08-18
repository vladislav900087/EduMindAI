import pytest
from sqlalchemy.exc import IntegrityError

from backend.app.models.user import User, UserRole
from backend.app.core.security import hash_password
from backend.app.models.lesson_progress import LessonProgress
from backend.app.models.lesson import Lesson
from backend.app.models.course import Course
from backend.app.repositories.lesson_progress_repository import LessonProgressRepository
from backend.app.repositories.course_repository import CourseRepository
from backend.app.repositories.lesson_repository import LessonRepository




def create_test_user(db_session, email: str, role: UserRole) -> User:
    test_user = User(email=email, role=role, hashed_password=hash_password('SuperSecretPassword123!'), full_name='Test User')

    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)

    return test_user

def save_user_to_db(db_session, test_user: User) -> User:

    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)

    return test_user

def save_course_to_db(db_session, course: Course) -> Course:

    db_session.add(course)
    db_session.commit()
    db_session.refresh(course)

    return course

def save_lesson_to_db(db_session, lesson: Lesson) -> Lesson:
    db_session.add(lesson)
    db_session.commit()
    db_session.refresh(lesson)

    return lesson

def save_lesson_progress_to_db(db_session, lesson_progress: LessonProgress) -> LessonProgress:

    db_session.add(lesson_progress)
    db_session.commit()
    db_session.refresh(lesson_progress)

    return lesson_progress


def test_create_lesson_progress(db_session):
    teacher = User(email='test_create_lesson_progress_teacher@example.com', hashed_password=hash_password('SuperSecretPassword123!'), full_name='Test Teacher', role=UserRole.TEACHER)

    teacher_saved = save_user_to_db(db_session, teacher)

    student = User(email='test_create_lesson_progress_student@example.com', hashed_password=hash_password('SuperSecretPassword123!'), full_name='Test Student', role=UserRole.STUDENT)

    student_saved = save_user_to_db(db_session, student)
    course = Course(title='Python course', description='Python Course for beginners.', teacher_id=teacher_saved.id)

    course_saved = save_course_to_db(db_session, course)

    lesson = Lesson(title='Python Basics', content='Python for beginners.', course_id=course_saved.id)

    lesson_saved = save_lesson_to_db(db_session, lesson)

    lesson_progress = LessonProgress(lesson_id=lesson_saved.id, student_id=student_saved.id)
    lesson_progress_repository = LessonProgressRepository(db_session)

    lesson_progress_saved = lesson_progress_repository.create(lesson_progress)

    assert lesson_progress_saved.lesson_id == lesson_saved.id
    assert lesson_progress_saved.student_id == student_saved.id


def test_get_progress_by_student_and_lesson(db_session):
    teacher = create_test_user(db_session, email='test_get_progress_by_student_and_lesson_teacher@example.com', role=UserRole.TEACHER)
    teacher_saved = save_user_to_db(db_session, teacher)

    student = create_test_user(db_session, email='test_get_progress_by_student_and_lesson_student@example.com', role=UserRole.STUDENT)
    student_saved = save_user_to_db(db_session, student)

    course = Course(title='Test course', description='Test course for beginners.', teacher_id=teacher_saved.id)

    course_saved = save_course_to_db(db_session, course)

    lesson = Lesson(title='Test lesson', content='Test lesson content', course_id=course_saved.id)
    lesson_saved = save_lesson_to_db(db_session, lesson)

    lesson_progress_repository = LessonProgressRepository(db_session)
    lesson_progress = LessonProgress(lesson_id=lesson_saved.id, student_id=student_saved.id)
    lesson_progress_saved = lesson_progress_repository.create(lesson_progress)


    assert lesson_progress_saved.lesson_id == lesson_saved.id
    assert lesson_progress_saved.student_id == student_saved.id

    returned_progress_record = lesson_progress_repository.get_by_student_and_lesson(student_id=student_saved.id,
                                                                                    lesson_id=lesson_saved.id)

    assert returned_progress_record.id == lesson_progress_saved.id
    assert returned_progress_record.student_id == student_saved.id
    assert returned_progress_record.lesson_id == lesson_saved.id


def test_list_progress_by_student_and_course(db_session):
    teacher = create_test_user(db_session, email='test_list_progress_by_student_teacher@example.com', role=UserRole.TEACHER)
    student = create_test_user(db_session, email='test_list_progress_by_student_test_student@example.com', role=UserRole.STUDENT)

    course_repository = CourseRepository(db_session)
    lesson_repository = LessonRepository(db_session)
    lesson_progress_repository = LessonProgressRepository(db_session)


    course = course_repository.create(Course(title='Great Course', description='The greatest Course ever created.', teacher_id=teacher.id))
    lesson_one = lesson_repository.create(Lesson(title='Great Lesson One', content='Great Lesson One content', course_id=course.id))
    lesson_two = lesson_repository.create(Lesson(title='Great Lesson Two', content='Great Lesson Two content', course_id=course.id))

    lesson_one_progress = lesson_progress_repository.create(LessonProgress(lesson_id=lesson_one.id, student_id=student.id))
    lesson_two_progress = lesson_progress_repository.create(LessonProgress(lesson_id=lesson_two.id, student_id=student.id))

    assert lesson_one_progress.lesson_id == lesson_one.id
    assert lesson_one_progress.student_id == student.id

    assert lesson_two_progress.lesson_id == lesson_two.id
    assert lesson_two_progress.student_id == student.id

    student_progress_in_course_lessons = lesson_progress_repository.list_by_student_and_course(student.id, course.id)

    assert len(student_progress_in_course_lessons) == 2
    assert student_progress_in_course_lessons[0].lesson_id == lesson_one.id
    assert student_progress_in_course_lessons[1].lesson_id == lesson_two.id


def test_list_progress_by_student(db_session):
    teacher = create_test_user(db_session, email='test_list_progress_by_student_test_teacher@example.com', role=UserRole.TEACHER)
    student_one = create_test_user(db_session, email='student_one@example.com', role=UserRole.STUDENT)
    student_two = create_test_user(db_session, email='student_two@example.com', role=UserRole.STUDENT)

    course_repository = CourseRepository(db_session)
    lesson_repository = LessonRepository(db_session)
    lesson_progress_repository = LessonProgressRepository(db_session)

    course = course_repository.create(Course(title='Some course', description='Some course description', teacher_id=teacher.id))

    first_lesson = lesson_repository.create(Lesson(title='Some lesson', content='Some lesson content', course_id=course.id))
    second_lesson = lesson_repository.create(Lesson(title='Second lesson', content='Second lesson content', course_id=course.id))

    first_lesson_progress_for_student_one = lesson_progress_repository.create(LessonProgress(lesson_id=first_lesson.id, student_id=student_one.id))
    second_lesson_progress_for_student_one = lesson_progress_repository.create(LessonProgress(lesson_id=second_lesson.id, student_id=student_one.id))
    lesson_progress_for_student_two = lesson_progress_repository.create(LessonProgress(lesson_id=first_lesson.id, student_id=student_two.id))

    assert first_lesson_progress_for_student_one.lesson_id == first_lesson.id
    assert first_lesson_progress_for_student_one.student_id == student_one.id

    assert second_lesson_progress_for_student_one.lesson_id == second_lesson.id
    assert second_lesson_progress_for_student_one.student_id == student_one.id

    assert lesson_progress_for_student_two.lesson_id == first_lesson.id
    assert lesson_progress_for_student_two.student_id == student_two.id

    returned_progress_records_for_student_one = lesson_progress_repository.list_by_student(student_one.id)

    assert len(returned_progress_records_for_student_one) == 2
    assert returned_progress_records_for_student_one[0].lesson_id == first_lesson.id
    assert returned_progress_records_for_student_one[0].student_id == student_one.id

    assert returned_progress_records_for_student_one[1].lesson_id == second_lesson.id
    assert returned_progress_records_for_student_one[1].student_id == student_one.id


def test_student_cannot_create_duplicate_lesson_progress(db_session):
    teacher = create_test_user(db_session, 'test_student_cannot_create_duplicate_lesson_progress_test_teacher@example.com', role=UserRole.TEACHER)
    student = create_test_user(db_session, 'test_student_cannot_create_duplicate_lesson_progress_test_student@example.com', role=UserRole.STUDENT)

    course_repository = CourseRepository(db_session)
    lesson_repository = LessonRepository(db_session)
    lesson_progress_repository = LessonProgressRepository(db_session)

    course = course_repository.create(Course(title='FastAPI Course', description='FastAPI Course description', teacher_id=teacher.id))
    lesson = lesson_repository.create(Lesson(title='FastAPI Lesson', content='FastAPI Lesson content', course_id=course.id))
    lesson_progress = lesson_progress_repository.create(LessonProgress(lesson_id=lesson.id, student_id=student.id))

    assert lesson_progress.lesson_id == lesson.id
    assert lesson_progress.student_id == student.id

    with pytest.raises(IntegrityError):
        duplicate_lesson_progress = lesson_progress_repository.create(LessonProgress(lesson_id=lesson.id, student_id=student.id))



















