import type { Currency } from '../types/payment';


export function formatMoney(
    amount: number,
    currency: Currency,
    ): string {
            return new Intl.NumberFormat(undefined, {
                    style: 'currency',
                    currency,
                    maximumFractionDigits: 0,
                }).format(amount);
        }


export function formatCoursePrice(
    amount: number,
    currency: Currency,
    ): string {

            if (amount === 0) {
                return 'Free';
                }

            return formatMoney(amount, currency);
        }