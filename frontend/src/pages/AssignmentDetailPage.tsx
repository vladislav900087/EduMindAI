import { useParams } from 'react-router-dom';


function AssignmentDetailPage() {

    const { assignmentId } = useParams();

    return (
        <section>
            <p className='text-sm font-medium text-blue-600'>Assignment</p>
            <h1 className='mt-2 text-2xl font-semibold text-slate-900'>Assignment #{assignmentId}</h1>
            <p className='mt-2 text-slate-600'>Assignment details and submission form will appear here.</p>

        </section>

        );


    }

export default AssignmentDetailPage;


