
import { useEffect, useState } from 'react';

import {
  createMockTopUp,
  getWalletBalance,
  getWalletTransactions,
} from '../api/walletApi';
import Button from '../components/ui/Button';
import { formatMoney } from '../utils/money';
import type {
  Currency,
  WalletBalance,
  WalletTransaction,
} from '../types/payment';

function WalletPage() {
  const [balance, setBalance] = useState<WalletBalance | null>(null);
  const [transactions, setTransactions] = useState<WalletTransaction[]>([]);
  const [amount, setAmount] = useState('');
  const [currency, setCurrency] = useState<Currency>('KZT');
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const isMockPaymentEnabled = import.meta.env.VITE_PAYMENT_PROVIDER === 'mock';

  async function loadWallet() {
    setErrorMessage('');
    setIsLoading(true);

    try {
      const [balanceData, transactionData] = await Promise.all([
        getWalletBalance(),
        getWalletTransactions(),
      ]);

      setBalance(balanceData);
      setTransactions(transactionData);
    } catch {
      setErrorMessage('Could not load wallet information.');
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    void loadWallet();
  }, []);

  async function handleTopUp() {
    const parsedAmount = Number(amount);

    if (!Number.isInteger(parsedAmount) || parsedAmount <= 0) {
      setErrorMessage('Enter a whole-number amount greater than zero.');
      return;
    }

    setErrorMessage('');
    setIsSubmitting(true);

    try {
      await createMockTopUp({
        amount: parsedAmount,
        currency,
      });

      setAmount('');
      await loadWallet();
    } catch {
      setErrorMessage('Could not add mock funds to the wallet.');
    } finally {
      setIsSubmitting(false);
    }
  }

  function getTransactionLabel(transaction: WalletTransaction): string {
    return transaction.transaction_type.replace('_', ' ');
  }

  if (isLoading) {
    return (
      <section className='rounded-lg border border-slate-200 bg-white p-6 text-sm text-slate-600 shadow-sm'>
        Loading wallet...
      </section>
    );
  }

  return (
    <section>
      <div>
        <p className='text-sm font-medium text-blue-600'>Payments</p>
        <h1 className='mt-2 text-2xl font-semibold text-slate-950'>
          Wallet
        </h1>
        <p className='mt-2 text-slate-600'>
          Review balances and transaction history.
        </p>
      </div>

      {errorMessage && (
        <p className='mt-6 rounded-md bg-red-50 px-4 py-3 text-sm text-red-700'>
          {errorMessage}
        </p>
      )}

      <div className='mt-6 grid gap-4 sm:grid-cols-2'>
        <section className='rounded-lg border border-slate-200 bg-white p-5 shadow-sm'>
          <p className='text-sm font-medium text-slate-600'>KZT balance</p>
          <p className='mt-2 text-2xl font-semibold text-slate-950'>
            {formatMoney(balance?.KZT ?? 0, 'KZT')}
          </p>
        </section>

        <section className='rounded-lg border border-slate-200 bg-white p-5 shadow-sm'>
          <p className='text-sm font-medium text-slate-600'>EUR balance</p>
          <p className='mt-2 text-2xl font-semibold text-slate-950'>
            {formatMoney(balance?.EUR ?? 0, 'EUR')}
          </p>
        </section>
      </div>
{isMockPaymentEnabled && (
                    <section className='mt-6 rounded-lg border border-slate-200 bg-white p-5 shadow-sm'>
                <h2 className='text-lg font-semibold text-slate-900'>
                  Add development funds
                </h2>

                <div className='mt-4 grid gap-4 sm:grid-cols-[1fr_120px_auto]'>
                  <input
                    className='rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100'
                    type='number'
                    min={1}
                    step={1}
                    value={amount}
                    onChange={(event) => setAmount(event.target.value)}
                    placeholder='Amount'
                  />

                  <select
                    className='rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100'
                    value={currency}
                    onChange={(event) =>
                      setCurrency(event.target.value as Currency)
                    }
                  >
                    <option value='KZT'>KZT</option>
                    <option value='EUR'>EUR</option>
                  </select>

                  <Button
                    type='button'
                    onClick={handleTopUp}
                    disabled={isSubmitting}
                  >
                    {isSubmitting ? 'Adding...' : 'Add funds'}
                  </Button>
                </div>
              </section>
              )}




      <section className='mt-6 rounded-lg border border-slate-200 bg-white p-5 shadow-sm'>
        <h2 className='text-lg font-semibold text-slate-900'>
          Transaction history
        </h2>

        {transactions.length === 0 ? (
          <p className='mt-4 text-sm text-slate-600'>
            No transactions yet.
          </p>
        ) : (
          <div className='mt-4 divide-y divide-slate-100'>
            {transactions.map((transaction) => {
              const isCredit = transaction.direction === 'credit';

              return (
                <div
                  key={transaction.id}
                  className='flex flex-wrap items-center justify-between gap-3 py-3'
                >
                  <div>
                    <p className='text-sm font-medium capitalize text-slate-900'>
                      {getTransactionLabel(transaction)}
                    </p>
                    <p className='mt-1 text-xs text-slate-500'>
                      {new Date(transaction.created_at).toLocaleString()}
                    </p>
                  </div>

                  <div className='text-right'>
                    <p
                      className={[
                        'text-sm font-semibold',
                        isCredit ? 'text-green-700' : 'text-slate-900',
                      ].join(' ')}
                    >
                      {isCredit ? '+' : '-'}
                      {formatMoney(
                        transaction.amount,
                        transaction.currency,
                      )}
                    </p>
                    <p className='mt-1 text-xs capitalize text-slate-500'>
                      {transaction.status}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </section>
    </section>
  );
}

export default WalletPage;