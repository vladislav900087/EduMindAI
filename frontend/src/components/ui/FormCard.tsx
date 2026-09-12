
import type { ReactNode } from 'react';

type FormCardProps = {

    title: string;
    children: ReactNode;

    };

function FormCard({ title, children }: FormCardProps) {

    return (
        <section className='rounded-lg border border-slate-200 bg-white p-5 shadow-sm'>
            <h2 className='text-lg font-semibold text-slate-900'>{title}</h2>
            <div className='mt-4'>
                {children}
            </div>
        </section>

        );

    }

export default FormCard;