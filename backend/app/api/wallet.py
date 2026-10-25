from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.api.security import get_current_user

from backend.app.models.user import User, UserRole


from backend.app.services.wallet_transaction_service import WalletTransactionService
from backend.app.api.dependencies import get_transaction_service, get_transaction_repository
from backend.app.schemas.wallet_transaction import WalletBalanceRead, WalletTransactionTopUp, WalletTransactionRead, TeacherWalletEarningsRead
from backend.app.repositories.wallet_transaction_repository import WalletTransactionRepository



router = APIRouter(prefix='/wallet', tags=['Wallet'])


@router.post('/mock-top-ups', response_model=WalletTransactionRead, status_code=status.HTTP_201_CREATED)
def create_wallet_mock_top_up(data: WalletTransactionTopUp, current_user: User = Depends(get_current_user),
                              service: WalletTransactionService = Depends(get_transaction_service)):
    try:
        return service.create_mock_top_up(user_id=current_user.id, amount=data.amount, currency=data.currency)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@router.get('/me', response_model=WalletBalanceRead)
def get_my_wallet_account(current_user: User = Depends(get_current_user), service: WalletTransactionService = Depends(get_transaction_service)):
    return service.get_balances(user_id=current_user.id)

@router.get('/me/transactions', response_model=list[WalletTransactionRead])
def list_user_wallet_transactions(current_user: User = Depends(get_current_user), repository: WalletTransactionRepository = Depends(get_transaction_repository)):

    return repository.list_transactions_by_user(user_id=current_user.id)

@router.get('/me/earnings', response_model=TeacherWalletEarningsRead)
def get_my_earnings(current_user: User = Depends(get_current_user), service: WalletTransactionService = Depends(get_transaction_service)):

    if current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only teachers can view their earnings')

    return service.get_teacher_earnings(teacher_id=current_user.id)




