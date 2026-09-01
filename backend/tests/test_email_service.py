from unittest.mock import patch, MagicMock
from backend.app.services.email_service import EmailService

@patch("smtplib.SMTP")
def test_send_email_success(mock_smtp):
    mock_server_instance = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_server_instance

    service = EmailService(
        host='smtp.test.com',
        port=587,
        username='test_user',
        password='test_password',
        from_email='sender@test.com',
        use_tls=True
    )

    service.send_email(recipient='receiver@test.com', subject='Test Subject', message_content='Hello Test')

    # assertions

    mock_smtp.assert_called_once_with('smtp.test.com', 587)
    mock_server_instance.starttls.assert_called_once()
    mock_server_instance.login.assert_called_once_with('test_user', 'test_password')
    mock_server_instance.send_message.assert_called_once()

@patch('smtplib.SMTP')
def test_send_email_without_tls(mock_smtp):

    mock_server_instance = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_server_instance

    service = EmailService(
        host='smtp.test.com',
        port=587,
        username='test_user',
        password='test_password',
        from_email='sender@test.com',
        use_tls=False
    )

    service.send_email(recipient='receiver@test.com', subject='Test Subject', message_content='Hello Test')

    mock_server_instance.starttls.assert_not_called()
    mock_server_instance.send_message.assert_called_once()













