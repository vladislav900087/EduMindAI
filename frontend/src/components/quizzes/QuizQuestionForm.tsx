import { type FormEvent, useState } from 'react';

import Button from '../ui/Button';
import type { QuizQuestionCreate } from '../../types/quiz';

type QuizQuestionFormProps = {
    onSubmit: (data: QuizQuestionCreate) => Promise<void>;
    }

function QuizQuestionForm({ onSubmit }: QuizQuestionFormProps) {

    const [questionText, setQuestionText] = useState('');
    const [options, setOptions] = useState(['', '', '', '']);
    const [correctIndex, setCorrectIndex] = useState(0);
    const [errorMessage, setErrorMessage] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);

    async function handleSubmit(event: FormEvent<HTMLFormElement>) {

        event.preventDefault();

        setErrorMessage('');

        const cleanedOptions = options.map((option) => option.trim());

        if (!questionText.trim()) {
            setErrorMessage('Question text is required.');
            return;
            }

        if (cleanedOptions.some((option) => !option)) {
            setErrorMessage('All options are required.');
            return;
            }

        setIsSubmitting(true);

        try {
            await onSubmit({
                question_text: questionText.trim(),
                options: cleanedOptions.map((option, index) => ({
                    option_text: option,
                    is_correct: index === correctIndex,
                    })),
                });
            setQuestionText('');
            setOptions(['', '', '', '']);
            setCorrectIndex(0);
            } catch {
                setErrorMessage('Could not create question.');
                } finally {
                    setIsSubmitting(false);
                    }


        }

    function updateOption(index: number, value: string) {

        setOptions((current) => current.map((option, optionIndex) => optionIndex === index ? value : option,
        ),
    );
  }

  return (
      <form className='space-y-4' onSubmit={handleSubmit}>
        <label className='block'>
            <span className='text-sm font-medium text-slate-700'>Question</span>
            <textarea
                className='mt-1 min-h-20 w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100'
                value={questionText}
                onChange={(event) => setQuestionText(event.target.value)}
                required
             />
        </label>

        <div className='space-y-3'>
            {options.map((option, index) => (
                <div key={index} className='flex gap-3'>
                    <input
                        className='mt-3'
                        type='radio'
                        name='correct-option'
                        checked={correctIndex === index}
                        onChange={() => setCorrectIndex(index)}
                     />

                     <input
                        className='w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100'
                        placeholder={`Option ${index + 1}`}
                        value={option}
                        onChange={(event) => updateOption(index, event.target.value)}
                        required
                      />
                </div>
                ))}
        </div>

        {errorMessage && (
            <p className='rounded-md bg-red-50 px-3 py-2 text-sm text-red-700'>
                {errorMessage}
            </p>
            )}
        <Button type='submit' disabled={isSubmitting}>
            {isSubmitting ? 'Adding...' : 'Add question'}

        </Button>
      </form>

      );
}

export default QuizQuestionForm;