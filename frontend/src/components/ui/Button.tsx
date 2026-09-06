import type { ButtonHTMLAttributes, ReactNode } from 'react';

type ButtonVariant = "primary" | "secondary" | "danger";

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {

    children: ReactNode;
    variant?: ButtonVariant;

    };

const variantClasses: Record<ButtonVariant, string> = {

    primary: 'bg-blue-600 text-white hover:bg-blue-700 disabled:bg-blue-300',
    secondary: 'border border-slate-300 bg-white text-slate-700 hover:bg-slate-100 disabled:text-slate-400',
    danger: 'bg-red-600 text-white hover:bg-red-700 disabled:bg-red-300'

    };

function Button({children, variant = 'primary', className='', ...props}: ButtonProps) {

    return (
        <button
            className={['rounded-md px-4 py-2 text-sm font-medium transition ',
                variantClasses[variant],
                className,
                ].join(" ")}
                {...props}
        >
            {children}
        </button>

        );

    }

export default Button;