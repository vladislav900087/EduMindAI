import { type FormEvent, useState } from 'react';
import { useTranslation } from 'react-i18next';

import type { Currency } from '../../types/payment';
import Button from '../ui/Button';

export type CourseFormValues = {
  title: string;
  description: string;
  price_amount: number;
  currency: Currency;
};

type CourseFormProps = {
  defaultCurrency: Currency;
  onSubmit: (values: CourseFormValues) => Promise<void>;
};

function CourseForm({
  defaultCurrency,
  onSubmit,
}: CourseFormProps) {
  const { t } = useTranslation();
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priceAmount, setPriceAmount] = useState('0');
  const [currency, setCurrency] = useState<Currency>(defaultCurrency);
  const [errorMessage, setErrorMessage] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setErrorMessage('');

    if (!title.trim()) {
      setErrorMessage('Course title is required.');
      return;
    }

    const parsedPriceAmount = Number(priceAmount);

    if (
      !Number.isInteger(parsedPriceAmount) ||
      parsedPriceAmount < 0 ||
      parsedPriceAmount > 100_000_000
    ) {
      setErrorMessage('Enter a whole-number price from 0 to 100000000.');
      return;
    }

    setIsSubmitting(true);

    try {
      await onSubmit({
        title: title.trim(),
        description: description.trim(),
        price_amount: parsedPriceAmount,
        currency,
      });

      setTitle('');
      setDescription('');
      setPriceAmount('0');
    } catch {
      setErrorMessage('Could not create course.');
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <form
      className='rounded-lg border border-slate-200 bg-white p-5 shadow-sm'
      onSubmit={handleSubmit}
    >
      <h2 className='text-lg font-semibold text-slate-900'>
        {t('work.createCourse')}
      </h2>

      <div className='mt-4 space-y-4'>
        <label className='block'>
          <span className='text-sm font-medium text-slate-700'>
            {t('work.title')}
          </span>
          <input
            className='mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100'
            type='text'
            value={title}
            onChange={(event) => setTitle(event.target.value)}
            maxLength={200}
            required
          />
        </label>

        <label className='block'>
          <span className='text-sm font-medium text-slate-700'>
            {t('work.description')}
          </span>
          <textarea
            className='mt-1 min-h-24 w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100'
            value={description}
            onChange={(event) => setDescription(event.target.value)}
          />
        </label>

        <div className='grid gap-4 sm:grid-cols-[1fr_120px]'>
          <label className='block'>
            <span className='text-sm font-medium text-slate-700'>
              Price
            </span>
            <input
              className='mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100'
              type='number'
              min={0}
              max={100000000}
              step={1}
              value={priceAmount}
              onChange={(event) => setPriceAmount(event.target.value)}
              required
            />
            <span className='mt-1 block text-xs text-slate-500'>
              Enter 0 for a free course.
            </span>
          </label>

          <label className='block'>
            <span className='text-sm font-medium text-slate-700'>
              Currency
            </span>
            <select
              className='mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100'
              value={currency}
              onChange={(event) =>
                setCurrency(event.target.value as Currency)
              }
            >
              <option value='KZT'>KZT</option>
              <option value='EUR'>EUR</option>
            </select>
          </label>
        </div>

        {errorMessage && (
          <p className='rounded-md bg-red-50 px-3 py-2 text-sm text-red-700'>
            {errorMessage}
          </p>
        )}

        <Button type='submit' disabled={isSubmitting}>
          {isSubmitting ? t('work.creating') : t('work.createCourse')}
        </Button>
      </div>
    </form>
  );
}

export default CourseForm;