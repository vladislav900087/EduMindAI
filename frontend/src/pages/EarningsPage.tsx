import { useState, useEffect } from 'react';
import { getTeacherEarnings } from '../api/walletApi';
import { formatMoney } from '../utils/money';
import type { TeacherEarnings } from '../types/payment';


function EarningsPage() {

            const [earnings, setEarnings] = useState<TeacherEarnings | null>(null);
            const [isLoading, setIsLoading] = useState(true);
            const [errorMessage, setErrorMessage] = useState('');

            useEffect(() => {

                    async function loadEarnings() {

                            setErrorMessage('');

                            try {
                                    const data = await getTeacherEarnings();
                                    setEarnings(data);
                                } catch {
                                    setErrorMessage('Could not load teacher earnings.')
                                    } finally {
                                        setIsLoading(false);
                                        }


                        }

                    void loadEarnings();
                }, [])

            if (isLoading) {
    return (
      <section className='rounded-lg border border-slate-200 bg-white p-6 text-sm text-slate-600 shadow-sm'>
        Loading earnings...
      </section>
    );
  }

  if (errorMessage) {
    return (
      <section className='rounded-lg border border-red-200 bg-red-50 p-6 text-sm text-red-700'>
        {errorMessage}
      </section>
    );
  }

  const transactions = earnings?.transactions ?? [];

  return (
    <section>
      <div>
        <p className='text-sm font-medium text-blue-600'>Payments</p>
        <h1 className='mt-2 text-2xl font-semibold text-slate-950'>
          Teacher earnings
        </h1>
        <p className='mt-2 text-slate-600'>
          Completed income from paid course sales.
        </p>
      </div>

      <div className='mt-6 grid gap-4 sm:grid-cols-2'>
        <section className='rounded-lg border border-slate-200 bg-white p-5 shadow-sm'>
          <p className='text-sm font-medium text-slate-600'>
            Total KZT earnings
          </p>
          <p className='mt-2 text-2xl font-semibold text-slate-950'>
            {formatMoney(earnings?.KZT ?? 0, 'KZT')}
          </p>
        </section>

        <section className='rounded-lg border border-slate-200 bg-white p-5 shadow-sm'>
          <p className='text-sm font-medium text-slate-600'>
            Total EUR earnings
          </p>
          <p className='mt-2 text-2xl font-semibold text-slate-950'>
            {formatMoney(earnings?.EUR ?? 0, 'EUR')}
          </p>
        </section>
      </div>

      <section className='mt-6 rounded-lg border border-slate-200 bg-white p-5 shadow-sm'>
        <h2 className='text-lg font-semibold text-slate-900'>
          Course sales
        </h2>

        {transactions.length === 0 ? (
          <p className='mt-4 text-sm text-slate-600'>
            No completed course sales yet.
          </p>
        ) : (
          <div className='mt-4 divide-y divide-slate-100'>
            {transactions.map((transaction) => (
              <div
                key={transaction.id}
                className='flex flex-wrap items-center justify-between gap-3 py-3'
              >
                <div>
                  <p className='text-sm font-medium text-slate-900'>
                    Course sale
                  </p>
                  <p className='mt-1 text-xs text-slate-500'>
                    {new Date(transaction.created_at).toLocaleString()}
                  </p>
                </div>

                <p className='text-sm font-semibold text-green-700'>
                  +{formatMoney(transaction.amount, transaction.currency)}
                </p>
              </div>
            ))}
          </div>
        )}
      </section>
    </section>
  );
}

export default EarningsPage;





