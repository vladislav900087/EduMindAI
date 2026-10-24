from backend.app.repositories.wallet_transaction_repository import WalletTransactionRepository
from backend.app.models.wallet_transaction import Currency, WalletTransactionDirection, WalletTransactionType, WalletTransaction
from backend.app.core.config import settings

class WalletTransactionService:
    def __init__(self, repository: WalletTransactionRepository):
        self.repository = repository

    def get_balances(self, user_id: int) -> dict[Currency, int]:

        balance = {
            Currency.KZT: 0,
            Currency.EUR: 0
        }

        transactions = self.repository.list_completed_by_user(user_id)

        for transaction in transactions:
            if transaction.direction == WalletTransactionDirection.CREDIT:
                balance[transaction.currency] += transaction.amount
            else:
                balance[transaction.currency] -= transaction.amount

        return balance

    def create_mock_top_up(self, user_id: int, amount: int, currency: Currency) -> WalletTransaction:

        if settings.payment_provider != 'mock':
            raise ValueError('Mock top-ups are unavailable.')

        wallet_transaction = WalletTransaction(user_id=user_id, amount=amount, currency=currency, direction=WalletTransactionDirection.CREDIT, transaction_type=WalletTransactionType.TOP_UP)

        self.repository.create(wallet_transaction)

        return wallet_transaction





