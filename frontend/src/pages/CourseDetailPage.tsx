import { useParams } from 'react-router-dom';


function CourseDetailPage() {

    const { courseId } = useParams();

    return (
        <section>
            <p className='text-sm font-medium text-blue-600'>Course</p>
            <h1 className='mt-2 text-2xl font-semibold text-slate-900'>Course #{courseId}</h1>
            <p className='mt-2 text-slate-600'>Course lessons, quizzes, and assignments will appear here.</p>

        </section>


        );


    }

export default CourseDetailPage;