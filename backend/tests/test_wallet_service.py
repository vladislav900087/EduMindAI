from backend.app.repositories.wallet_transaction_repository import WalletTransactionRepository
from backend.app.services.wallet_transaction_service import WalletTransactionService

from backend.tests.test_courses_api import create_test_user
from backend.app.models.user import UserRole

def test_user_with_no_transactions(db_session):

    user = create_test_user(db_session, 'test_user@example.com', role=UserRole.STUDENT)

    service = WalletTransactionService(WalletTransactionRepository(db_session))

    user_balances = service.get_balances(user_id=user.id)

    assert user_balances['KZT'] == 0
    assert user_balances['EUR'] == 0

