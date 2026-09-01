from unittest.mock import MagicMock, patch

from backend.app.tasks.deadlines import send_assignment_deadline_reminders

def test_send_assignment_deadline_reminders_task_returns_sent_count_message():
    with patch('backend.app.tasks.deadlines.SessionLocal') as session_local_mock, patch('backend.app.tasks.deadlines.AssignmentDeadlineReminderService') as service_class_mock:
        db_mock = MagicMock()
        session_local_mock.return_value = db_mock

        service_mock = MagicMock()
        service_mock.send_24_hour_reminders.return_value = 2
        service_class_mock.return_value = service_mock

        result = send_assignment_deadline_reminders.run()

        assert result == f'Sent 2 assignment deadline reminder(s).'
        service_mock.send_24_hour_reminders.assert_called_once()
        db_mock.close.assert_called_once()







