from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.wallet_transaction import WalletTransaction, WalletTransactionStatus


class WalletTransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, wallet_transaction: WalletTransaction) -> WalletTransaction:
        self.db.add(wallet_transaction)
        self.db.commit()
        self.db.refresh(wallet_transaction)

        return wallet_transaction

    def create_without_commit(self, wallet_transaction: WalletTransaction) -> WalletTransaction:

        self.db.add(wallet_transaction)
        self.db.flush()

        return wallet_transaction

    def list_completed_by_user(self, user_id: int) -> list[WalletTransaction]:
        statement = select(WalletTransaction).where(WalletTransaction.user_id == user_id, WalletTransaction.status == WalletTransactionStatus.COMPLETED).order_by(WalletTransaction.created_at.asc())

        return list(self.db.scalars(statement))

    def list_transactions_by_user(self, user_id: int) -> list[WalletTransaction]:

        statement = select(WalletTransaction).where(WalletTransaction.user_id == user_id).order_by(WalletTransaction.created_at.desc())

        return list(self.db.scalars(statement))



