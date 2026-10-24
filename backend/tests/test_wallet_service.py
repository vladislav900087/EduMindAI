from backend.app.repositories.wallet_transaction_repository import WalletTransactionRepository
from backend.app.services.wallet_transaction_service import WalletTransactionService

from backend.tests.test_courses_api import create_test_user
from backend.app.models.user import UserRole
from backend.app.models.wallet_transaction import WalletTransaction, WalletTransactionType, WalletTransactionDirection, WalletTransactionStatus
from backend.app.models.course_purchase import Currency
from backend.app.repositories.course_repository import CourseRepository
from backend.app.repositories.course_enrollment_repository import CourseEnrollmentRepository
from backend.app.repositories.user_repository import UserRepository
from backend.app.repositories.course_purchase_repository import CoursePurchaseRepository
from backend.app.services.course_purchase_service import CoursePurchaseService
from backend.app.models.user import User, UserRole
from backend.app.models.course import Course, CourseStatus
from backend.app.models.course_enrollment import CourseEnrollment
from backend.app.models.course_purchase import CoursePurchase, PurchaseStatus
from backend.app.models.wallet_transaction import WalletTransaction
from backend.app.core.security import hash_password

import pytest

def test_user_with_no_transactions(db_session):

    user = create_test_user(db_session, 'test_user@example.com', role=UserRole.STUDENT)

    service = WalletTransactionService(WalletTransactionRepository(db_session))

    user_balances = service.get_balances(user_id=user.id)

    assert user_balances['KZT'] == 0
    assert user_balances['EUR'] == 0

def test_user_with_completed_kzt_credit(db_session):

    user = create_test_user(db_session, 'test_user@example.com', role=UserRole.STUDENT)

    service = WalletTransactionService(WalletTransactionRepository(db_session))
    repository = WalletTransactionRepository(db_session)

    transaction = WalletTransaction(user_id=user.id, amount=1000, currency=Currency.KZT, transaction_type=WalletTransactionType.TOP_UP, direction=WalletTransactionDirection.CREDIT, status=WalletTransactionStatus.COMPLETED)

    db_session.add(transaction)
    db_session.commit()
    db_session.refresh(transaction)



    assert transaction.user_id == user.id
    assert transaction.amount == 1000
    assert transaction.status == WalletTransactionStatus.COMPLETED

    balance = repository.list_completed_by_user(user_id=user.id)

    assert len(balance) == 1
    assert balance[0].amount == 1000
    assert balance[0].status == WalletTransactionStatus.COMPLETED

    user_balances = service.get_balances(user_id=user.id)
    assert user_balances['KZT'] == 1000

def test_user_with_completed_debit(db_session):

    user = create_test_user(db_session, email='test_user@example.com', role=UserRole.STUDENT)

    repository = WalletTransactionRepository(db_session)
    service = WalletTransactionService(WalletTransactionRepository(db_session))

    wallet_transaction_credit = WalletTransaction(user_id=user.id, amount=1000, currency=Currency.KZT, transaction_type=WalletTransactionType.TOP_UP, direction=WalletTransactionDirection.CREDIT, status=WalletTransactionStatus.COMPLETED)
    wallet_transaction_debit = WalletTransaction(user_id=user.id, amount=1000, currency=Currency.KZT, transaction_type=WalletTransactionType.PAYOUT, direction=WalletTransactionDirection.DEBIT, status=WalletTransactionStatus.COMPLETED)

    repository.create(wallet_transaction_credit)

    user_balances = service.get_balances(user_id=user.id)

    assert user_balances['KZT'] == 1000

    repository.create(wallet_transaction=wallet_transaction_debit)

    user_balances = service.get_balances(user_id=user.id)

    assert user_balances['KZT'] == 0

def test_pending_and_failed_wallet_transactions(db_session):

    user = create_test_user(db_session, email='test@example.com', role=UserRole.STUDENT)

    repository = WalletTransactionRepository(db_session)
    service = WalletTransactionService(repository)

    wallet_transaction_credit = WalletTransaction(user_id=user.id, amount=10000, currency=Currency.KZT, transaction_type=WalletTransactionType.TOP_UP, direction=WalletTransactionDirection.CREDIT, status=WalletTransactionStatus.COMPLETED)

    repository.create(wallet_transaction_credit)

    failed_transaction = WalletTransaction(user_id=user.id, amount=10000, currency=Currency.KZT, transaction_type=WalletTransactionType.PAYOUT, direction=WalletTransactionDirection.DEBIT, status=WalletTransactionStatus.FAILED)

    repository.create(failed_transaction)

    pending_transaction = WalletTransaction(user_id=user.id, amount=1000000, currency=Currency.KZT, transaction_type=WalletTransactionType.TOP_UP, direction=WalletTransactionDirection.CREDIT, status=WalletTransactionStatus.PENDING)

    repository.create(pending_transaction)

    user_balances = service.get_balances(user_id=user.id)

    assert user_balances['KZT'] == 10000

def test_kzt_and_eur_wallet_transactions(db_session):

    user = create_test_user(db_session, email='test@example.com', role=UserRole.STUDENT)

    repository = WalletTransactionRepository(db_session)

    service = WalletTransactionService(repository)

    kzt_transaction = WalletTransaction(user_id=user.id, amount=1000, currency=Currency.KZT, transaction_type=WalletTransactionType.TOP_UP, direction=WalletTransactionDirection.CREDIT, status=WalletTransactionStatus.COMPLETED)

    repository.create(kzt_transaction)

    eur_transaction = WalletTransaction(user_id=user.id, amount=1000, currency=Currency.EUR, transaction_type=WalletTransactionType.TOP_UP, direction=WalletTransactionDirection.CREDIT, status=WalletTransactionStatus.COMPLETED)


    repository.create(eur_transaction)

    user_balances = service.get_balances(user_id=user.id)

    assert user_balances['KZT'] == 1000
    assert user_balances['EUR'] == 1000

def test_student_with_enough_kzt_can_buy_kzt_course(db_session):

    user_repository = UserRepository(db_session)
    course_repository = CourseRepository(db_session)
    enrollment_repository = CourseEnrollmentRepository(db_session)
    transaction_repository = WalletTransactionRepository(db_session)
    purchase_repository = CoursePurchaseRepository(db_session)
    purchase_service = CoursePurchaseService(course_repository=course_repository, enrollment_repository=enrollment_repository, transaction_repository=transaction_repository, purchase_repository=purchase_repository, user_repository=user_repository, db=db_session)

    student = User(email='test_student@example.com', hashed_password=hash_password('SuperSecretPassword123'), role=UserRole.STUDENT, full_name='Test Student')
    user_repository.create(student)

    teacher = User(email='test_teacher@example.com', hashed_password=hash_password('SuperSecretPassword123'), role=UserRole.TEACHER, full_name='Test Teacher')
    user_repository.create(teacher)

    course = Course(title='Course title', description='Course description', price_amount=10000, currency=Currency.KZT, teacher_id=teacher.id, status=CourseStatus.PUBLISHED)

    course_repository.create(course)

    student_top_up = WalletTransaction(user_id=student.id, amount=10000, currency=Currency.KZT, transaction_type=WalletTransactionType.TOP_UP, direction=WalletTransactionDirection.CREDIT, status=WalletTransactionStatus.COMPLETED)

    transaction_repository.create(student_top_up)

    student_balance = {
        Currency.KZT: 0,
        Currency.EUR: 0
    }

    student_transactions = transaction_repository.list_completed_by_user(student.id)

    for transaction in student_transactions:
        if transaction.direction == WalletTransactionDirection.CREDIT:
            student_balance[transaction.currency] += transaction.amount
        else:
            student_balance[transaction.currency] -= transaction.amount

    assert student_balance['KZT'] == 10000
    assert student_balance['EUR'] == 0

    course_purchase = purchase_service.purchase_course(course_id=course.id, student_id=student.id)

    assert course_purchase is not None
    assert course_purchase.course_id == course.id
    assert course_purchase.student_id == student.id
    assert course_purchase.teacher_id == teacher.id
    assert course_purchase.price_amount == course.price_amount
    assert course_purchase.currency == course.currency
    assert course_purchase.status == PurchaseStatus.COMPLETED

    student_balance = {
        Currency.KZT: 0,
        Currency.EUR: 0,
    }

    student_transactions = transaction_repository.list_completed_by_user(student.id)

    for transaction in student_transactions:
        if transaction.direction == WalletTransactionDirection.CREDIT:
            student_balance[transaction.currency] += transaction.amount
        else:
            student_balance[transaction.currency] -= transaction.amount

    assert student_balance[Currency.KZT] == 0
    assert student_balance[Currency.EUR] == 0

    student_enrollment = enrollment_repository.get_by_student_and_course(student_id=student.id, course_id=course.id)

    assert student_enrollment is not None
    assert student_enrollment.student_id == student.id
    assert student_enrollment.course_id == course.id

    teacher_balance = {
        Currency.KZT: 0,
        Currency.EUR: 0
    }

    teacher_transactions = transaction_repository.list_completed_by_user(teacher.id)

    for transaction in teacher_transactions:
        if transaction.direction == WalletTransactionDirection.CREDIT:
            teacher_balance[transaction.currency] += transaction.amount
        else:
            teacher_balance[transaction.currency] -= transaction.amount

    assert teacher_balance[Currency.KZT] == 10000
    assert teacher_balance[Currency.EUR] == 0

def test_student_with_insufficient_balance_cannot_buy_course(db_session):

    user_repository = UserRepository(db_session)
    course_repository = CourseRepository(db_session)
    enrollment_repository = CourseEnrollmentRepository(db_session)
    transaction_repository = WalletTransactionRepository(db_session)
    purchase_repository = CoursePurchaseRepository(db_session)

    purchase_service = CoursePurchaseService(user_repository=user_repository, course_repository=course_repository, enrollment_repository=enrollment_repository, transaction_repository=transaction_repository, purchase_repository=purchase_repository, db=db_session)

    student = User(email='test_student@example.com', role=UserRole.STUDENT, full_name='Test Student', hashed_password=hash_password('SuperSecretPassword123'))

    user_repository.create(student)

    teacher = User(email='test_teacher@example.com', role=UserRole.TEACHER, full_name='Test Teacher', hashed_password=hash_password('SuperSecretHashedPassword123'))

    user_repository.create(teacher)

    course = Course(title='Course title', description='Course description', price_amount=10000, currency=Currency.KZT, teacher_id=teacher.id, status=CourseStatus.PUBLISHED)

    course_repository.create(course)

    student_transactions = transaction_repository.list_completed_by_user(student.id)

    student_balance = {
        Currency.KZT: 0,
        Currency.EUR: 0,
    }

    for transaction in student_transactions:
        if transaction.direction == WalletTransactionDirection.CREDIT:
            student_balance[transaction.currency] += transaction.amount
        else:
            student_balance[transaction.currency] -= transaction.amount

    assert student_balance[Currency.KZT] == 0
    assert student_balance[Currency.EUR] == 0

    assert len(student_transactions) == 0

    with pytest.raises(ValueError, match='Insufficient wallet balance'):
        purchase_service.purchase_course(student_id=student.id, course_id=course.id)



def test_student_cannot_buy_the_same_course_twice(db_session):

    user_repository = UserRepository(db_session)
    course_repository = CourseRepository(db_session)
    enrollment_repository = CourseEnrollmentRepository(db_session)
    transaction_repository = WalletTransactionRepository(db_session)
    purchase_repository = CoursePurchaseRepository(db_session)

    purchase_service = CoursePurchaseService(user_repository=user_repository, course_repository=course_repository, enrollment_repository=enrollment_repository, purchase_repository=purchase_repository, db=db_session, transaction_repository=transaction_repository)

    student = User(email='test_student@example.com', role=UserRole.STUDENT, full_name='Test Student', hashed_password=hash_password('SuperSecretPassword123'))

    user_repository.create(student)

    teacher = User(email='test_teacher@example.com', role=UserRole.TEACHER, full_name='Test Teacher', hashed_password=hash_password('SuperSecretHashedPassword123'))

    user_repository.create(teacher)

    course = Course(title='Course title', description='Course description', price_amount=10000, currency=Currency.KZT, teacher_id=teacher.id, status=CourseStatus.PUBLISHED)

    course_repository.create(course)

    student_top_up = WalletTransaction(user_id=student.id, amount=10000, currency=Currency.KZT, transaction_type=WalletTransactionType.TOP_UP, direction=WalletTransactionDirection.CREDIT, status=WalletTransactionStatus.COMPLETED)

    transaction_repository.create(student_top_up)

    student_balance = {
        Currency.KZT: 0,
        Currency.EUR: 0,
    }

    student_transactions = transaction_repository.list_completed_by_user(student.id)

    for transaction in student_transactions:
        if transaction.direction == WalletTransactionDirection.CREDIT:
            student_balance[transaction.currency] += transaction.amount
        else:
            student_balance[transaction.currency] -= transaction.amount

    assert student_balance[Currency.KZT] == 10000
    assert student_balance[Currency.EUR] == 0

    course_purchase = purchase_service.purchase_course(student_id=student.id, course_id=course.id)

    assert course_purchase.course_id == course.id
    assert course_purchase.student_id == student.id
    assert course_purchase.status == PurchaseStatus.COMPLETED
    assert course_purchase.price_amount == course.price_amount

    student_enrollment = enrollment_repository.get_by_student_and_course(student_id=student.id, course_id=course.id)

    assert student_enrollment is not None
    assert student_enrollment.course_id == course.id
    assert student_enrollment.student_id == student.id

    student_balance = {
        Currency.KZT: 0,
        Currency.EUR: 0,
    }

    student_transactions = transaction_repository.list_completed_by_user(student.id)

    for transaction in student_transactions:
        if transaction.direction == WalletTransactionDirection.CREDIT:
            student_balance[transaction.currency] += transaction.amount
        else:
            student_balance[transaction.currency] -= transaction.amount

    assert student_balance[Currency.KZT] == 0
    assert student_balance[Currency.EUR] == 0

    teacher_balance = {
        Currency.KZT: 0,
        Currency.EUR: 0,
    }

    teacher_transactions = transaction_repository.list_completed_by_user(teacher.id)

    for transaction in teacher_transactions:
        if transaction.direction == WalletTransactionDirection.CREDIT:
            teacher_balance[transaction.currency] += transaction.amount
        else:
            teacher_balance[transaction.currency] -= transaction.amount

    assert teacher_balance[Currency.KZT] == 10000
    assert teacher_balance[Currency.EUR] == 0

    with pytest.raises(ValueError, match='Course already purchased'):
        purchase_service.purchase_course(student_id=student.id, course_id=course.id)

def test_student_cannot_buy_draft_course(db_session):

    user_repository = UserRepository(db_session)
    course_repository = CourseRepository(db_session)
    enrollment_repository = CourseEnrollmentRepository(db_session)
    transaction_repository = WalletTransactionRepository(db_session)
    purchase_repository = CoursePurchaseRepository(db_session)

    purchase_service = CoursePurchaseService(user_repository=user_repository, course_repository=course_repository, enrollment_repository=enrollment_repository, transaction_repository=transaction_repository, purchase_repository=purchase_repository, db=db_session)

    student = User(email='test_student@example.com', hashed_password=hash_password('SuperSecretPassword123'), role=UserRole.STUDENT, full_name='Test Student')

    user_repository.create(student)

    teacher = User(email='test_teacher@example.com', hashed_password=hash_password('SuperSecretHashedPassword123'), role=UserRole.TEACHER, full_name='Test Teacher')

    user_repository.create(teacher)

    course = Course(title='Course title', description='Course description', teacher_id=teacher.id, status=CourseStatus.DRAFT, price_amount=10000, currency=Currency.KZT)

    course_repository.create(course)

    student_top_up = WalletTransaction(user_id=student.id, currency=Currency.KZT, amount=10000, transaction_type=WalletTransactionType.TOP_UP, direction=WalletTransactionDirection.CREDIT, status=WalletTransactionStatus.COMPLETED)

    transaction_repository.create(student_top_up)

    student_balance = {
        Currency.KZT: 0,
        Currency.EUR: 0,
    }

    student_transactions = transaction_repository.list_completed_by_user(user_id=student.id)

    for transaction in student_transactions:
        if transaction.direction == WalletTransactionDirection.CREDIT:
            student_balance[transaction.currency] += transaction.amount
        else:
            student_balance[transaction.currency] -= transaction.amount

    assert student_balance[Currency.KZT] == 10000
    assert student_balance[Currency.EUR] == 0

    with pytest.raises(ValueError, match='Only published courses can be purchased'):
        purchase_service.purchase_course(student_id=student.id, course_id=course.id)

def test_student_cannot_buy_a_free_course_through_this_endpoint(db_session):

    user_repository = UserRepository(db_session)
    course_repository = CourseRepository(db_session)
    enrollment_repository = CourseEnrollmentRepository(db_session)
    transaction_repository = WalletTransactionRepository(db_session)
    purchase_repository = CoursePurchaseRepository(db_session)

    purchase_service = CoursePurchaseService(db=db_session, user_repository=user_repository, course_repository=course_repository, enrollment_repository=enrollment_repository, transaction_repository=transaction_repository, purchase_repository=purchase_repository)

    student = User(email='test_student@example.com', hashed_password=hash_password('SuperSecretPassword123'), role=UserRole.STUDENT, full_name='Test Student')

    user_repository.create(student)

    teacher = User(email='test_teacher@example.com', hashed_password=hash_password('SuperSecretHashedTeacherPassword123'), role=UserRole.TEACHER, full_name='Test Teacher')

    user_repository.create(teacher)

    course = Course(title='Course title', description='Course description', teacher_id=teacher.id, price_amount=0, currency=Currency.KZT, status=CourseStatus.PUBLISHED)

    course_repository.create(course)

    student_top_up = WalletTransaction(user_id=student.id, amount=10000, currency=Currency.KZT, transaction_type=WalletTransactionType.TOP_UP, direction=WalletTransactionDirection.CREDIT, status=WalletTransactionStatus.COMPLETED)

    transaction_repository.create(student_top_up)

    student_balance = {
        Currency.KZT: 0,
        Currency.EUR: 0,
    }

    student_transactions = transaction_repository.list_completed_by_user(user_id=student.id)

    for transaction in student_transactions:
        if transaction.direction == WalletTransactionDirection.CREDIT:
            student_balance[transaction.currency] += transaction.amount
        else:
            student_balance[transaction.currency] -= transaction.amount

    assert student_balance[Currency.KZT] == 10000
    assert student_balance[Currency.EUR] == 0

    with pytest.raises(ValueError, match='Free courses must use the existing enrollment route'):
        purchase_service.purchase_course(student_id=student.id, course_id=course.id)

def test_failed_purchase_leaves_both_wallets_unchanged(db_session):

    user_repository = UserRepository(db_session)
    course_repository = CourseRepository(db_session)
    enrollment_repository = CourseEnrollmentRepository(db_session)
    transaction_repository = WalletTransactionRepository(db_session)
    purchase_repository = CoursePurchaseRepository(db_session)

    purchase_service = CoursePurchaseService(db=db_session, user_repository=user_repository, course_repository=course_repository, enrollment_repository=enrollment_repository, transaction_repository=transaction_repository, purchase_repository=purchase_repository)

    student = User(email='test_student@example.com', role=UserRole.STUDENT, full_name='Test Student', hashed_password=hash_password('SuperSecretPassword123'))

    user_repository.create(student)

    teacher = User(email='test_teacher@example.com', role=UserRole.TEACHER, full_name='Test Teacher', hashed_password=hash_password('SuperSecretHashedTeacherPassword123'))

    user_repository.create(teacher)

    course = Course(title='Course title', description='Course description', teacher_id=teacher.id, price_amount=0, currency=Currency.KZT, status=CourseStatus.PUBLISHED)

    course_repository.create(course)

    student_top_up = WalletTransaction(user_id=student.id, amount=10000, currency=Currency.KZT, transaction_type=WalletTransactionType.TOP_UP, direction=WalletTransactionDirection.CREDIT, status=WalletTransactionStatus.COMPLETED)

    transaction_repository.create(student_top_up)

    teacher_top_up = WalletTransaction(user_id=teacher.id, amount=1000, currency=Currency.EUR, transaction_type=WalletTransactionType.TOP_UP, direction=WalletTransactionDirection.CREDIT, status=WalletTransactionStatus.COMPLETED)

    transaction_repository.create(teacher_top_up)

    student_balance = {
        Currency.KZT: 0,
        Currency.EUR: 0,
    }

    student_transactions = transaction_repository.list_completed_by_user(user_id=student.id)

    for transaction in student_transactions:
        if transaction.direction == WalletTransactionDirection.CREDIT:
            student_balance[transaction.currency] += transaction.amount
        else:
            student_balance[transaction.currency] -= transaction.amount

    teacher_balance = {
        Currency.KZT: 0,
        Currency.EUR: 0,
    }
    teacher_transactions = transaction_repository.list_completed_by_user(user_id=teacher.id)

    for transaction in teacher_transactions:
        if transaction.direction == WalletTransactionDirection.CREDIT:
            teacher_balance[transaction.currency] += transaction.amount
        else:
            teacher_balance[transaction.currency] -= transaction.amount

    assert teacher_balance[Currency.KZT] == 0
    assert teacher_balance[Currency.EUR] == 1000

    with pytest.raises(ValueError, match='Free courses must use the existing enrollment route'):
        purchase_service.purchase_course(course_id=course.id, student_id=student.id)

    student_balance = {
        Currency.KZT: 0,
        Currency.EUR: 0,
    }

    student_transactions = transaction_repository.list_completed_by_user(user_id=student.id)

    for transaction in student_transactions:
        if transaction.direction == WalletTransactionDirection.CREDIT:
            student_balance[transaction.currency] += transaction.amount
        else:
            student_balance[transaction.currency] -= transaction.amount

    assert student_balance[Currency.KZT] == 10000
    assert student_balance[Currency.EUR] == 0

    teacher_balance = {
        Currency.KZT: 0,
        Currency.EUR: 0,
    }

    teacher_transactions = transaction_repository.list_completed_by_user(user_id=teacher.id)

    for transaction in teacher_transactions:
        if transaction.direction == WalletTransactionDirection.CREDIT:
            teacher_balance[transaction.currency] += transaction.amount
        else:
            teacher_balance[transaction.currency] -= transaction.amount

    assert teacher_balance[Currency.KZT] == 0
    assert teacher_balance[Currency.EUR] == 1000


def test_kzt_funds_cannot_purchase_an_euro_course(db_session):

    user_repository = UserRepository(db_session)
    course_repository = CourseRepository(db_session)
    enrollment_repository = CourseEnrollmentRepository(db_session)
    transaction_repository = WalletTransactionRepository(db_session)
    purchase_repository = CoursePurchaseRepository(db_session)

    purchase_service = CoursePurchaseService(db=db_session, user_repository=user_repository, course_repository=course_repository, enrollment_repository=enrollment_repository, transaction_repository=transaction_repository, purchase_repository=purchase_repository)

    student = User(email='test_student@example.com', role=UserRole.STUDENT, full_name='Test Student', hashed_password=hash_password('SuperSecretPassword123'))

    user_repository.create(student)

    teacher = User(email='test_teacher@example.com', role=UserRole.TEACHER, full_name='Test Teacher', hashed_password=hash_password('SuperSecretHashedTeacherPassword123!'))

    user_repository.create(teacher)

    course = Course(title='Course title', description='Course description', teacher_id=teacher.id, price_amount=20, currency=Currency.EUR, status=CourseStatus.PUBLISHED)

    course_repository.create(course)

    student_top_up = WalletTransaction(user_id=student.id, amount=10000, currency=Currency.KZT, transaction_type=WalletTransactionType.TOP_UP, direction=WalletTransactionDirection.CREDIT, status=WalletTransactionStatus.COMPLETED)

    transaction_repository.create(student_top_up)

    student_balance = {
        Currency.KZT: 0,
        Currency.EUR: 0,
    }

    student_transactions = transaction_repository.list_completed_by_user(user_id=student.id)

    for transaction in student_transactions:
        if transaction.direction == WalletTransactionDirection.CREDIT:
            student_balance[transaction.currency] += transaction.amount
        else:
            student_balance[transaction.currency] -= transaction.amount

    assert student_balance[Currency.KZT] == 10000
    assert student_balance[Currency.EUR] == 0

    with pytest.raises(ValueError, match='Insufficient wallet balance'):
        purchase_service.purchase_course(course_id=course.id, student_id=student.id)


    student_balance = {
        Currency.KZT: 0,
        Currency.EUR: 0,
    }

    for transaction in student_transactions:
        if transaction.direction == WalletTransactionDirection.CREDIT:
            student_balance[transaction.currency] += transaction.amount
        else:
            student_balance[transaction.currency] -= transaction.amount

    assert student_balance[Currency.KZT] == 10000
    assert student_balance[Currency.EUR] == 0

    teacher_balance = {
        Currency.KZT: 0,
        Currency.EUR: 0,
    }

    teacher_transactions = transaction_repository.list_completed_by_user(user_id=teacher.id)

    for transaction in teacher_transactions:
        if transaction.direction == WalletTransactionDirection.CREDIT:
            teacher_balance[transaction.currency] += transaction.amount
        else:
            teacher_balance[transaction.currency] -= transaction.amount

    assert teacher_balance[Currency.KZT] == 0
    assert teacher_balance[Currency.EUR] == 0

























