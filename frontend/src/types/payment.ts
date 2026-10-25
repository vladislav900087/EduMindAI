
export type Currency = 'KZT' | 'EUR';


export type WalletTransactionType =
        | 'top_up'
        | 'course_purchase'
        | 'course_sale'
        | 'refund'
        | 'payout';

export type WalletTransactionDirection = 'credit' | 'debit';

export type WalletTransactionStatus = 'pending' | 'completed' | 'failed';

export type WalletBalance = {
    KZT: number;
    EUR: number;
    };

export type WalletTransaction = {

    id: number;
    purchase_id: number | null;
    amount: number;
    currency: Currency;
    transaction_type: WalletTransactionType;
    direction: WalletTransactionDirection;
    status: WalletTransactionStatus;
    created_at: string;

    };

export type MockTopUpRequest = {
    amount: number;
    currency: Currency;
    };

export type TeacherEarnings = {

    KZT: number;
    EUR: number;
    transactions: WalletTransaction[];
    };

export type CoursePurchase = {
    id: number;
    student_id: number;
    teacher_id: number;
    course_id: number;
    price_amount: number;
    currency: Currency;
    status: 'completed' | 'refunded';
    purchased_at: string;
    };


