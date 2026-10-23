from backend.app.repositories.wallet_transaction_repository import WalletTransactionRepository
from backend.app.models.wallet_transaction import Currency

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
            if transaction.direction == 'CREDIT':
                balance[transaction.currency] += transaction.amount
            if transaction.direction == 'DEBIT':
                balance[transaction.currency] -= transaction.amount

        return balance
