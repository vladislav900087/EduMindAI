from backend.tests.test_quiz_attempt_api import create_test_user_and_login
from backend.app.models.user import UserRole
from backend.app.repositories.wallet_transaction_repository import WalletTransactionRepository
from backend.app.models.wallet_transaction import WalletTransaction, WalletTransactionStatus, WalletTransactionType, WalletTransactionDirection, Currency
from backend.app.core.config import settings
from backend.app.repositories.user_repository import UserRepository
from backend.app.models.course import CourseStatus
from backend.app.models.course_purchase import PurchaseStatus





def test_user_can_get_their_wallet_account(db_session, client):

    token = create_test_user_and_login(db_session, client, UserRole.STUDENT)

    response = client.get('/wallet/me', headers={"Authorization": f'Bearer {token}'})

    assert response.status_code == 200
    assert response.json()['KZT'] == 0
    assert response.json()['EUR'] == 0

def test_user_can_get_their_calculated_balances(db_session, client):

    user, token = create_test_user_and_login(db_session, client, UserRole.STUDENT, include_user=True)

    repository = WalletTransactionRepository(db_session)

    transaction_kzt = WalletTransaction(user_id=user.id, amount=100000, currency=Currency.KZT, transaction_type=WalletTransactionType.TOP_UP, status=WalletTransactionStatus.COMPLETED, direction=WalletTransactionDirection.CREDIT)

    repository.create(transaction_kzt)

    transaction_eur = WalletTransaction(user_id=user.id, amount=1000, currency=Currency.EUR, transaction_type=WalletTransactionType.TOP_UP, status=WalletTransactionStatus.COMPLETED, direction=WalletTransactionDirection.CREDIT)

    repository.create(transaction_eur)

    response = client.get('/wallet/me', headers={"Authorization": f'Bearer {token}'})

    assert response.status_code == 200
    assert response.json()['KZT'] == 100000
    assert response.json()['EUR'] == 1000

def test_unauthenticated_user_gets_401(client):

    response = client.get('/wallet/me')

    assert response.status_code == 401

def test_pending_and_failed_transactions_do_not_affect_the_users_balances(db_session, client):

    user, token = create_test_user_and_login(db_session, client, UserRole.TEACHER, include_user=True)

    repository = WalletTransactionRepository(db_session)

    kzt_top_up = WalletTransaction(user_id=user.id, amount=1000, currency=Currency.KZT, transaction_type=WalletTransactionType.TOP_UP, direction=WalletTransactionDirection.CREDIT, status=WalletTransactionStatus.COMPLETED)

    repository.create(kzt_top_up)

    failed_transaction_kzt = WalletTransaction(user_id=user.id, amount=1000, currency=Currency.KZT, transaction_type=WalletTransactionType.PAYOUT, direction=WalletTransactionDirection.DEBIT, status=WalletTransactionStatus.FAILED)

    repository.create(failed_transaction_kzt)

    pending_transaction_eur = WalletTransaction(user_id=user.id, amount=3000, currency=Currency.EUR, transaction_type=WalletTransactionType.TOP_UP, direction=WalletTransactionDirection.CREDIT, status=WalletTransactionStatus.PENDING)

    repository.create(pending_transaction_eur)

    response = client.get('/wallet/me', headers={"Authorization": f'Bearer {token}'})

    assert response.status_code == 200

    assert response.json()['KZT'] == 1000
    assert response.json()['EUR'] == 0


def test_student_can_create_kzt_mock_top_up_and_their_wallet_balance_increases(db_session, client):

    token = create_test_user_and_login(db_session, client, UserRole.STUDENT)

    top_up_response = client.post('/wallet/mock-top-ups', headers={'Authorization': f'Bearer {token}'}, json={'amount': 1000, 'currency': Currency.KZT})

    assert top_up_response.status_code == 201

    assert top_up_response.json()['amount'] == 1000

    get_balances_response = client.get('/wallet/me', headers={"Authorization": f'Bearer {token}'})

    assert get_balances_response.status_code == 200
    assert get_balances_response.json()['KZT'] == 1000

def test_teacher_can_create_eur_mock_top_up_and_their_eur_balance_increases(db_session, client):

    token = create_test_user_and_login(db_session, client, UserRole.TEACHER)

    top_up_response = client.post('/wallet/mock-top-ups', headers={'Authorization': f'Bearer {token}'}, json={'amount': 1000, 'currency': Currency.EUR})

    assert top_up_response.status_code == 201

    assert top_up_response.json()['amount'] == 1000
    assert top_up_response.json()['currency'] == Currency.EUR

    get_balances_response = client.get('/wallet/me', headers={'Authorization': f'Bearer {token}'})

    assert get_balances_response.status_code == 200
    assert get_balances_response.json()['EUR'] == 1000

    assert get_balances_response.json()['KZT'] == 0

def test_zero_and_negative_amounts_return_validation_error(db_session, client):

    token = create_test_user_and_login(db_session, client, UserRole.TEACHER)

    top_up_response = client.post('/wallet/mock-top-ups', headers={'Authorization': f'Bearer {token}'}, json={'amount': -1000, 'currency': Currency.EUR})

    assert top_up_response.status_code == 422

def test_unauthenticated_top_up_request_returns_401(client):

    response = client.post('/wallet/mock-top-ups')

    assert response.status_code == 401

def test_if_payment_provider_is_not_mock_endpoint_refuses_to_create_money(db_session, client):

    settings.payment_provider = 'non-mock provider'

    token = create_test_user_and_login(db_session, client, UserRole.STUDENT)

    response = client.post('/wallet/mock-top-ups', headers={'Authorization': f'Bearer {token}'}, json={'amount': 1000, 'currency': Currency.KZT})

    assert response.status_code == 400

    settings.payment_provider = 'mock'

def test_student_with_enough_balance_receives_201_while_purchasing_course(db_session, client):

    create_student_response = client.post('/auth/register', json={'email': 'test_student@example.com', 'password': 'SuperSecretPassword123', 'full_name': 'Test Student'})

    assert create_student_response.status_code == 201

    assert create_student_response.json()['role'] == UserRole.STUDENT

    login_student_response = client.post('/auth/login', data={'username': 'test_student@example.com', 'password': 'SuperSecretPassword123'})

    assert login_student_response.status_code == 200

    student_token = login_student_response.json()['access_token']

    create_teacher_response = client.post('/auth/register', json={'email': 'test_teacher@example.com', 'password': 'SuperSecretHashedPassword123', 'full_name': 'Test Teacher'})

    assert create_teacher_response.status_code == 201

    teacher_id = create_teacher_response.json()['id']

    user_repository = UserRepository(db_session)

    teacher = user_repository.get_by_id(teacher_id)

    teacher.role = UserRole.TEACHER

    user_repository.update(teacher)

    teacher_login_response = client.post('/auth/login', data={'username': 'test_teacher@example.com', 'password': 'SuperSecretHashedPassword123'})

    assert teacher_login_response.status_code == 200

    teacher_token = teacher_login_response.json()['access_token']

    teachers_get_me_response = client.get('/users/me', headers={'Authorization': f'Bearer {teacher_token}'})

    assert teachers_get_me_response.status_code == 200
    assert teachers_get_me_response.json()['role'] == UserRole.TEACHER

    course_create_response = client.post('/courses', headers={'Authorization': f'Bearer {teacher_token}'}, json={'title': 'Course title', 'description': 'Course description', 'price_amount': 10000, 'currency': Currency.KZT})

    assert course_create_response.status_code == 201

    course_id = course_create_response.json()['id']

    publish_course_response = client.post(f'/courses/{course_id}/publish', headers={'Authorization': f'Bearer {teacher_token}'})

    assert publish_course_response.status_code == 200

    assert publish_course_response.json()['status'] == CourseStatus.PUBLISHED

    student_top_up_response = client.post('/wallet/mock-top-ups', headers={'Authorization': f'Bearer {student_token}'}, json={'amount': 10000, 'currency': Currency.KZT})

    assert student_top_up_response.status_code == 201

    student_get_balance_response = client.get('/wallet/me', headers={'Authorization': f'Bearer {student_token}'})

    assert student_get_balance_response.status_code == 200
    assert student_get_balance_response.json()['KZT'] == 10000

    student_course_purchase_response = client.post(f'/courses/{course_id}/purchase', headers={'Authorization': f'Bearer {student_token}'})

    assert student_course_purchase_response.status_code == 201


    assert student_course_purchase_response.json()['price_amount'] == 10000
    assert student_course_purchase_response.json()['currency'] == Currency.KZT
    assert student_course_purchase_response.json()['course_id'] == course_id
    assert student_course_purchase_response.json()['student_id'] == create_student_response.json()['id']
    assert student_course_purchase_response.json()['status'] == PurchaseStatus.COMPLETED

    student_get_balance_response = client.get('/wallet/me', headers={'Authorization': f'Bearer {student_token}'})

    assert student_get_balance_response.status_code == 200
    assert student_get_balance_response.json()['KZT'] == 0

    teacher_get_balance_response = client.get('/wallet/me', headers={'Authorization': f'Bearer {teacher_token}'})

    assert teacher_get_balance_response.status_code == 200
    assert teacher_get_balance_response.json()['KZT'] == 10000
    assert teacher_get_balance_response.json()['EUR'] == 0

def test_unauthenticated_purchase_request_receives_401(client):

    response = client.post('/courses/999999/purchase')

    assert response.status_code == 401


def test_teacher_purchase_request_receives_403(client, db_session):

    create_teacher_response = client.post('/auth/register', json={'email': 'test_teacher@example.com', 'password': 'SuperSecretHashedTeacherPassword123', 'full_name': 'Test Teacher'})

    assert create_teacher_response.status_code == 201

    teacher_id = create_teacher_response.json()['id']

    teacher_login_response = client.post('/auth/login', data={'username': 'test_teacher@example.com', 'password': 'SuperSecretHashedTeacherPassword123'})

    assert teacher_login_response.status_code == 200
    teacher_token = teacher_login_response.json()['access_token']

    user_repository = UserRepository(db_session)

    teacher = user_repository.get_by_id(teacher_id)

    teacher.role = UserRole.TEACHER

    user_repository.update(teacher)

    teachers_get_me_response = client.get('/users/me', headers={'Authorization': f'Bearer {teacher_token}'})

    assert teachers_get_me_response.status_code == 200
    assert teachers_get_me_response.json()['role'] == UserRole.TEACHER

    course_purchase_attempt_response = client.post('/courses/999999/purchase', headers={'Authorization': f'Bearer {teacher_token}'})

    assert course_purchase_attempt_response.status_code == 403

def test_students_insufficient_funds_receives_400_and_creates_no_record(client, db_session):

    student_create_response = client.post('/auth/register', json={'email': 'test_student_email@exmaple.com', 'password': 'SuperSecretHashedStudentPassword123', 'full_name': 'Test Student'})

    assert student_create_response.status_code == 201

    student_login_response = client.post('/auth/login', data={'username': 'test_student_email@exmaple.com', 'password': 'SuperSecretHashedStudentPassword123'})

    assert student_login_response.status_code == 200

    student_token = student_login_response.json()['access_token']

    teacher_create_response = client.post('/auth/register', json={'email': 'test_teacher_email@example.com', 'password': 'SuperSecretHashedTeacherPassword123', 'full_name': 'Test Teacher'})

    assert teacher_create_response.status_code == 201

    teacher_id = teacher_create_response.json()['id']

    teacher_login_response = client.post('/auth/login', data={'username': 'test_teacher_email@example.com', 'password': 'SuperSecretHashedTeacherPassword123'})

    assert teacher_login_response.status_code == 200

    teacher_token = teacher_login_response.json()['access_token']

    user_repository = UserRepository(db_session)

    teacher = user_repository.get_by_id(teacher_id)

    teacher.role = UserRole.TEACHER

    user_repository.update(teacher)

    teachers_get_me_response = client.get('/users/me', headers={'Authorization': f'Bearer {teacher_token}'})

    assert teachers_get_me_response.status_code == 200
    assert teachers_get_me_response.json()['role'] == UserRole.TEACHER

    create_course_response = client.post('/courses', headers={'Authorization': f'Bearer {teacher_token}'}, json={'title': 'Test Course', 'description': 'Test Course Description', 'price_amount': 10000, 'currency': Currency.KZT})

    assert create_course_response.status_code == 201

    course_id = create_course_response.json()['id']

    publish_course_response = client.post(f'/courses/{course_id}/publish', headers={'Authorization': f'Bearer {teacher_token}'})

    assert publish_course_response.status_code == 200

    student_get_balance_response = client.get('/wallet/me', headers={'Authorization': f'Bearer {student_token}'})

    assert student_get_balance_response.status_code == 200
    assert student_get_balance_response.json()['KZT'] == 0

    student_purchase_attempt_response = client.post(f'/courses/{course_id}/purchase', headers={"Authorization": f'Bearer {student_token}'})

    assert student_purchase_attempt_response.status_code == 400

    teacher_get_balance_response = client.get('/wallet/me', headers={'Authorization': f'Bearer {teacher_token}'})

    assert teacher_get_balance_response.status_code == 200
    assert teacher_get_balance_response.json()['KZT'] == 0

    student_get_their_enrollments_response = client.get('/enrollments/me', headers={"Authorization": f'Bearer {student_token}'})

    assert student_get_their_enrollments_response.status_code == 200
    assert len(student_get_their_enrollments_response.json()) == 0

def test_missing_course_receives_404(client, db_session):

    create_student_response = client.post('/auth/register', json={'email': 'test_student@example.com', 'password': 'SuperSecretHashedStudentPassword123!', 'full_name': 'Test Student'})

    assert create_student_response.status_code == 201

    login_student_response = client.post('/auth/login', data={'username': 'test_student@example.com', 'password': 'SuperSecretHashedStudentPassword123!'})

    assert login_student_response.status_code == 200

    student_token = login_student_response.json()['access_token']

    student_purchase_attempt_response = client.post('/courses/999999/purchase', headers={'Authorization': f'Bearer {student_token}'})

    assert student_purchase_attempt_response.status_code == 404

def test_duplicate_purchase_attempt_receives_400(client, db_session):

    create_teacher_response = client.post('/auth/register', json={'email': 'test_teacher@example.com', 'password': 'SuperSecretHashedTeacherPassword123!', 'full_name': 'Test Teacher'})

    assert create_teacher_response.status_code == 201

    teacher_login_response = client.post('/auth/login', data={'username': 'test_teacher@example.com', 'password': 'SuperSecretHashedTeacherPassword123!'})

    assert teacher_login_response.status_code == 200

    teacher_token = teacher_login_response.json()['access_token']

    teacher_get_me_response = client.get('/users/me', headers={'Authorization': f'Bearer {teacher_token}'})

    assert teacher_get_me_response.status_code == 200

    teacher_id = teacher_get_me_response.json()['id']

    user_repository = UserRepository(db_session)

    teacher = user_repository.get_by_id(teacher_id)

    teacher.role = UserRole.TEACHER

    user_repository.update(teacher)

    create_student_response = client.post('/auth/register', json={'email': 'test_student@example.com', 'password': 'SuperSecretHashedStudentPassword123!', 'full_name': 'Test Student'})

    assert create_student_response.status_code == 201

    login_student_response = client.post('/auth/login', data={"username": 'test_student@example.com', 'password': 'SuperSecretHashedStudentPassword123!'})

    assert login_student_response.status_code == 200

    student_token = login_student_response.json()['access_token']

    create_course_response = client.post('/courses', headers={'Authorization': f'Bearer {teacher_token}'}, json={'title': 'Course title', 'description': 'Course description', 'price_amount': 10000, 'currency': Currency.KZT})

    assert create_course_response.status_code == 201

    course_id = create_course_response.json()['id']

    publish_course_response = client.post(f'/courses/{course_id}/publish', headers={'Authorization': f'Bearer {teacher_token}'})

    assert publish_course_response.status_code == 200

    student_top_up_response = client.post('/wallet/mock-top-ups', headers={'Authorization': f'Bearer {student_token}'}, json={'amount': 10000, 'currency': Currency.KZT})

    assert student_top_up_response.status_code == 201

    student_get_balance_response = client.get('/wallet/me', headers={'Authorization': f'Bearer {student_token}'})

    assert student_get_balance_response.status_code == 200

    assert student_get_balance_response.json()['KZT'] == 10000

    student_course_purchase_response = client.post(f'/courses/{course_id}/purchase', headers={'Authorization': f'Bearer {student_token}'})

    assert student_course_purchase_response.status_code == 201

    student_get_balances_response = client.get('/wallet/me', headers={'Authorization': f'Bearer {student_token}'})

    assert student_get_balances_response.status_code == 200
    assert student_get_balances_response.json()['KZT'] == 0

    student_top_up_response = client.post('/wallet/mock-top-ups', headers={'Authorization': f'Bearer {student_token}'}, json={'amount': 10000, 'currency': Currency.KZT})

    assert student_top_up_response.status_code == 201

    student_get_balances_response = client.get('/wallet/me', headers={"Authorization": f'Bearer {student_token}'})

    assert student_get_balances_response.status_code == 200

    assert student_get_balances_response.json()['KZT'] == 10000

    student_duplicate_purchase_attempt = client.post(f'/courses/{course_id}/purchase', headers={"Authorization": f'Bearer {student_token}'})

    assert student_duplicate_purchase_attempt.status_code == 400

    student_get_balances_response = client.get('/wallet/me', headers={'Authorization': f'Bearer {student_token}'})

    assert student_get_balances_response.status_code == 200
    assert student_get_balances_response.json()['KZT'] == 10000

    teacher_get_balances_response = client.get('/wallet/me', headers={"Authorization": f'Bearer {teacher_token}'})

    assert teacher_get_balances_response.status_code == 200
    assert teacher_get_balances_response.json()['KZT'] == 10000

def test_new_user_receives_empty_transaction_list(db_session, client):

    user_token = create_test_user_and_login(db_session, client, role=UserRole.STUDENT)

    response = client.get('/wallet/me/transactions', headers={'Authorization': f'Bearer {user_token}'})

    assert response.status_code == 200
    assert len(response.json()) == 0

def test_user_receives_only_their_records(db_session, client):

    user_one_token = create_test_user_and_login(db_session, client, role=UserRole.STUDENT)
    user_two_token = create_test_user_and_login(db_session, client, role=UserRole.TEACHER)

    create_course_response = client.post('/courses', headers={"Authorization": f'Bearer {user_two_token}'}, json={'title': 'Course title', 'description': 'Course description', 'price_amount': 10000, 'currency': Currency.KZT})

    assert create_course_response.status_code == 201

    course_id = create_course_response.json()['id']

    publish_course_response = client.post(f'/courses/{course_id}/publish', headers={'Authorization': f'Bearer {user_two_token}'})

    assert publish_course_response.status_code == 200

    top_up_response = client.post('/wallet/mock-top-ups', headers={'Authorization': f'Bearer {user_one_token}'}, json={'amount': 10000, 'currency': Currency.KZT})

    assert top_up_response.status_code == 201

    get_balances_response = client.get('/wallet/me', headers={"Authorization": f'Bearer {user_one_token}'})

    assert get_balances_response.status_code == 200

    assert get_balances_response.json()['KZT'] == 10000

    purchase_course_response = client.post(f'/courses/{course_id}/purchase', headers={'Authorization': f'Bearer {user_one_token}'})

    assert purchase_course_response.status_code == 201

    get_student_transaction_history_response = client.get('/wallet/me/transactions', headers={'Authorization': f'Bearer {user_one_token}'})

    assert get_student_transaction_history_response.status_code == 200

    assert len(get_student_transaction_history_response.json()) == 2
    assert get_student_transaction_history_response.json()[0]['transaction_type'] == WalletTransactionType.COURSE_PURCHASE

    get_teacher_history_response = client.get('/wallet/me/transactions', headers={"Authorization": f'Bearer {user_two_token}'})

    assert get_teacher_history_response.status_code == 200

    assert len(get_teacher_history_response.json()) == 1

    assert get_teacher_history_response.json()[0]['transaction_type'] == WalletTransactionType.COURSE_SALE





































