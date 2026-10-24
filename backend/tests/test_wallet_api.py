from backend.tests.test_quiz_attempt_api import create_test_user_and_login
from backend.app.models.user import UserRole
from backend.app.repositories.wallet_transaction_repository import WalletTransactionRepository
from backend.app.models.wallet_transaction import WalletTransaction, WalletTransactionStatus, WalletTransactionType, WalletTransactionDirection, Currency
from backend.app.core.config import settings



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









