import { useParams } from 'react-router-dom';


function QuizTakingPage() {

    const { quizId } = useParams();

    return (
        <section>
            <p className='text-sm font-medium text-blue-600'>Quiz</p>
            <h1 className='mt-2 text-2xl font-semibold text-slate-900'>Quiz #{quizId}</h1>
            <p className='mt-2 text-slate-600'>Quiz questions will appear here.</p>

        </section>

        );



    }

export default QuizTakingPage;