from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, Integer, String, func, CheckConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column

from backend.app.db.database import Base

from backend.app.models.course import Currency

class WalletTransactionType(str, Enum):
    TOP_UP = 'top_up'
    COURSE_PURCHASE = 'course_purchase'
    COURSE_SALE = 'course_sale'
    REFUND = 'refund'
    PAYOUT = 'payout'

class WalletTransactionDirection(str, Enum):
    CREDIT = 'credit'
    DEBIT = 'debit'

class WalletTransactionStatus(str, Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'

class WalletTransaction(Base):
    __tablename__ = 'wallet_transactions'

    __table_args__ = (
        CheckConstraint('amount > 0', name='ck_wallet_transaction_price_amount_positive'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False, index=True)
    purchase_id: Mapped[int | None] = mapped_column(ForeignKey('course_purchases.id'), nullable=True, index=True)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[Currency] = mapped_column(String(3), nullable=False)
    transaction_type: Mapped[WalletTransactionType] = mapped_column(String(30), nullable=False)
    direction: Mapped[WalletTransactionDirection] = mapped_column(String(10), nullable=False)
    status: Mapped[WalletTransactionStatus] = mapped_column(String(20), nullable=False, default=WalletTransactionStatus.COMPLETED, server_default=WalletTransactionStatus.COMPLETED.value)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    user = relationship('User')
    purchase = relationship('CoursePurchase')




