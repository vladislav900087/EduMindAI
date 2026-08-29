from backend.tests.test_assignment_repository import create_test_environment
from backend.tests.test_quiz_attempt_api import create_test_user_and_login, login_user
from backend.app.models.user import UserRole
import uuid

def test_teacher_can_create_assignment_for_own_course(db_session, client):
    teacher, course, assignment_repository = create_test_environment(db_session)
    teacher_token = login_user(client, teacher.email)
    uid = uuid.uuid4().hex[:8]

    response = client.post(f'/assignments/courses/{course.id}', headers={"Authorization": f'Bearer {teacher_token}'}, json={'title': f'Test Assignment {uid}', 'description': 'Test Assignment Description', 'due_at': None})
    assert response.status_code == 201


def test_teacher_cannot_create_assignment_for_another_teachers_course(db_session, client):
    teacher_a, course, assignment_repository = create_test_environment(db_session)

    teacher_b_token = create_test_user_and_login(db_session, client=client, role=UserRole.TEACHER)

    response = client.post(f'/assignments/courses/{course.id}', headers={'Authorization': f'Bearer {teacher_b_token}'}, json={'title': f'Test Assignment {uuid.uuid4().hex[:8]}'})
    assert response.status_code == 403

def test_admin_can_create_assignment_for_any_course(db_session, client):
    teacher, course, assignment_repository = create_test_environment(db_session)
    admin_token = create_test_user_and_login(db_session, client=client, role=UserRole.ADMIN)
    uid = uuid.uuid4().hex[:8]

    response = client.post(f'/assignments/courses/{course.id}', headers={'Authorization': f'Bearer {admin_token}'}, json={'title': f'Test Assignment {uid}'})
    assert response.status_code == 201

def test_student_cannot_create_assignment(db_session, client):
    teacher, course, assignment_repository = create_test_environment(db_session)
    student_token = create_test_user_and_login(db_session, client=client, role=UserRole.STUDENT)

    response = client.post(f'/assignments/courses/{course.id}', headers={"Authorization": f'Bearer {student_token}'}, json={'title': 'Test Assignment'})

    assert response.status_code == 403

def test_student_can_list_course_assignments(db_session, client):
    teacher, course, assignment_repository = create_test_environment(db_session)
    teacher_token = login_user(client, teacher.email)
    student_token = create_test_user_and_login(db_session, client=client, role=UserRole.STUDENT)
    uid = uuid.uuid4().hex[:8]

    create_response = client.post(f'/assignments/courses/{course.id}', headers={'Authorization': f'Bearer {teacher_token}'}, json={'title': f'Test Assignment {uid}'})
    assert create_response.status_code == 201

    retrieve_response = client.get(f'/assignments/courses/{course.id}', headers={'Authorization': f'Bearer {student_token}'})

    assert retrieve_response.status_code == 200

def test_teacher_can_list_course_assignments(db_session, client):
    teacher, course, assignment_repository = create_test_environment(db_session)
    teacher_token = login_user(client, teacher.email)

    response = client.get(f'/assignments/courses/{course.id}', headers={'Authorization': f'Bearer {teacher_token}'})
    assert response.status_code == 200

def test_get_assignment(db_session, client):
    teacher, course, assignment_repository = create_test_environment(db_session)
    teacher_token = login_user(client, teacher.email)
    uid = uuid.uuid4().hex[:8]

    create_response = client.post(f'/assignments/courses/{course.id}', headers={"Authorization": f'Bearer {teacher_token}'}, json={'title': f'Test Assignment {uid}'})
    assert create_response.status_code == 201

    data = create_response.json()
    assignment_id = data['id']

    assert assignment_id

    get_response = client.get(f'/assignments/{assignment_id}')

    assert get_response.status_code == 200

def test_get_missing_assignment(db_session, client):

    response = client.get('/assignments/999999')

    assert response.status_code == 404

def test_teacher_can_update_own_assignment(db_session, client):
    teacher, course, assignment_repository = create_test_environment(db_session)
    teacher_token = login_user(client, teacher.email)

    uid = uuid.uuid4().hex[:8]

    create_response = client.post(f'/assignments/courses/{course.id}', headers={'Authorization': f'Bearer {teacher_token}'}, json={'title': f'Test Assignment {uid}'})

    assert create_response.status_code == 201

    data = create_response.json()
    assignment_id = data['id']

    update_response = client.put(f'/assignments/{assignment_id}', headers={'Authorization': f'Bearer {teacher_token}'}, json={'title': f'New Title {uid}'})
    assert update_response.status_code == 200

    updated_data = update_response.json()
    assert updated_data['title'] != data['title']
    assert updated_data['id'] == assignment_id
    assert updated_data['title'] == f'New Title {uid}'


def test_teacher_cannot_update_another_teachers_assignment(db_session, client):
    teacher_a, course, assignment_repository = create_test_environment(db_session)
    teacher_a_token = login_user(client, teacher_a.email)
    teacher_b_token = create_test_user_and_login(db_session, client=client, role=UserRole.TEACHER)

    uid = uuid.uuid4().hex[:8]

    create_response = client.post(f'/assignments/courses/{course.id}', headers={'Authorization': f'Bearer {teacher_a_token}'}, json={'title': f'Test Assignment {uid}'})

    assert create_response.status_code == 201

    assignment_id = create_response.json()['id']

    update_response = client.put(f'/assignments/{assignment_id}', headers={'Authorization': f'Bearer {teacher_b_token}'}, json={'title': f'New Title {uid}'})

    assert update_response.status_code == 403

def test_admin_can_update_any_assignment(db_session, client):
    teacher, course, assignment_repository = create_test_environment(db_session)
    teacher_token = login_user(client, teacher.email)
    admin_token = create_test_user_and_login(db_session, client=client, role=UserRole.ADMIN)

    uid = uuid.uuid4().hex[:8]

    create_response = client.post(f'/assignments/courses/{course.id}', headers={"Authorization": f'Bearer {teacher_token}'}, json={"title": f'Assignment Title {uid}'})

    assert create_response.status_code == 201

    assignment_id = create_response.json()['id']

    update_response = client.put(f'/assignments/{assignment_id}', headers={'Authorization': f'Bearer {admin_token}'}, json={'title': f'New Title {uid}'})

    assert update_response.status_code == 200


def test_teacher_can_delete_own_assignment(db_session, client):
    teacher, course, assignment_repository = create_test_environment(db_session)
    teacher_token = login_user(client, teacher.email)

    uid = uuid.uuid4().hex[:8]

    create_response = client.post(f'/assignments/courses/{course.id}', headers={'Authorization': f'Bearer {teacher_token}'}, json={'title': f'Test Assignment {uid}'})
    assert create_response.status_code == 201

    assignment_id = create_response.json()['id']

    delete_response = client.delete(f'/assignments/{assignment_id}', headers={'Authorization': f'Bearer {teacher_token}'})

    assert delete_response.status_code == 204


def test_teacher_cannot_delete_another_teachers_assignment(db_session, client):
    teacher_a, course, assignment_repository = create_test_environment(db_session)
    teacher_a_token = login_user(client, teacher_a.email)
    teacher_b_token = create_test_user_and_login(db_session, client=client, role=UserRole.TEACHER)

    uid = uuid.uuid4().hex[:8]

    create_response = client.post(f'/assignments/courses/{course.id}', headers={'Authorization': f'Bearer {teacher_a_token}'}, json={'title': f'Test Assignment {uid}'})

    assert create_response.status_code == 201

    assignment_id = create_response.json()['id']

    delete_response = client.delete(f'/assignments/{assignment_id}', headers={"Authorization": f'Bearer {teacher_b_token}'})
    assert delete_response.status_code == 403

def test_admin_can_delete_any_assignment(db_session, client):
    teacher, course, assignment_repository = create_test_environment(db_session)
    teacher_token = login_user(client, teacher.email)
    admin_token = create_test_user_and_login(db_session, client=client, role=UserRole.ADMIN)

    uid = uuid.uuid4().hex[:8]

    create_response = client.post(f'/assignments/courses/{course.id}', headers={'Authorization': f'Bearer {teacher_token}'}, json={'title': f'Assignment Title {uid}'})

    assert create_response.status_code == 201

    assignment_id = create_response.json()['id']

    delete_response = client.delete(f'/assignments/{assignment_id}', headers={'Authorization': f'Bearer {admin_token}'})

    assert delete_response.status_code == 204










