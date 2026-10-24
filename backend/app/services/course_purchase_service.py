from backend.app.models.course_purchase import CoursePurchase, Currency, PurchaseStatus
from backend.app.repositories.course_purchase_repository import CoursePurchaseRepository
from backend.app.repositories.course_enrollment_repository import CourseEnrollmentRepository
from backend.app.repositories.wallet_transaction_repository import WalletTransactionRepository
from backend.app.repositories.course_repository import CourseRepository
from backend.app.repositories.user_repository import UserRepository
from sqlalchemy.orm import Session
from backend.app.models.course import CourseStatus
from backend.app.models.wallet_transaction import WalletTransaction, WalletTransactionDirection, WalletTransactionType, WalletTransactionStatus
from backend.app.models.course_enrollment import CourseEnrollment



class CoursePurchaseService:
    def __init__(self, db: Session, purchase_repository: CoursePurchaseRepository, enrollment_repository: CourseEnrollmentRepository, transaction_repository: WalletTransactionRepository, course_repository: CourseRepository, user_repository: UserRepository):

        self.db = db
        self.purchase_repository = purchase_repository
        self.enrollment_repository = enrollment_repository
        self.transaction_repository = transaction_repository
        self.course_repository = course_repository
        self.user_repository = user_repository

    def purchase_course(self, student_id: int, course_id: int) -> CoursePurchase:

        try:
            student = self.user_repository.get_by_id_for_update(user_id=student_id)
            if student is None:
                raise ValueError('Student not found')
            course = self.course_repository.get_by_id(course_id)
            if course is None:
                raise ValueError('Course not found')

            if course.status != CourseStatus.PUBLISHED:
                raise ValueError('Only published courses can be purchased')

            current_course_purchase = self.purchase_repository.get_purchase(student_id=student_id, course_id=course_id)

            if course.price_amount == 0:
                raise ValueError('Free courses must use the existing enrollment route')

            if current_course_purchase is not None:
                raise ValueError('Course already purchased')

            current_course_enrollment = self.enrollment_repository.get_by_student_and_course(student_id=student_id, course_id=course_id)

            if current_course_enrollment is not None:
                raise ValueError('Student is already enrolled to this course')

            student_completed_transactions = self.transaction_repository.list_completed_by_user(student_id)


            balance = {
                Currency.KZT: 0,
                Currency.EUR: 0,

            }

            for transaction in student_completed_transactions:
                if transaction.direction == WalletTransactionDirection.CREDIT:
                    balance[transaction.currency] += transaction.amount
                else:
                    balance[transaction.currency] -= transaction.amount

            if course.price_amount > balance[course.currency]:
                raise ValueError('Insufficient wallet balance')

            current_teacher = course.teacher
            if current_teacher is None:
                raise ValueError('Teacher not found')


            current_purchase = self.purchase_repository.create_without_commit(CoursePurchase(student_id=student_id, course_id=course.id, teacher_id=course.teacher_id, price_amount=course.price_amount, status=PurchaseStatus.COMPLETED, currency=course.currency))
            self.transaction_repository.create_without_commit(WalletTransaction(user_id=student_id, amount=course.price_amount, purchase_id=current_purchase.id, currency=course.currency, transaction_type=WalletTransactionType.COURSE_PURCHASE, direction=WalletTransactionDirection.DEBIT, status=WalletTransactionStatus.COMPLETED))



            self.transaction_repository.create_without_commit(WalletTransaction(user_id=course.teacher_id, amount=course.price_amount, purchase_id=current_purchase.id, currency=course.currency, transaction_type=WalletTransactionType.COURSE_SALE, direction=WalletTransactionDirection.CREDIT, status=WalletTransactionStatus.COMPLETED))

            self.enrollment_repository.create_without_commit(CourseEnrollment(student_id=student_id, course_id=course.id))

            self.db.commit()

            return current_purchase

        except Exception as exc:
            self.db.rollback()
            raise ValueError(exc) from exc












