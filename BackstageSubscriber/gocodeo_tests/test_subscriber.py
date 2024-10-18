import os
import pytest
from unittest import mock
from google.cloud import pubsub_v1
from loguru import logger
from Infrastructure.RepositoryKeeper import TransactionRepository
from BackstageSubscriber.subscriber import callback

@pytest.fixture
def mock_environment():
    with mock.patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": "mocked_path.json"}):
        yield

@pytest.fixture
def mock_subscriber_client():
    with mock.patch('google.cloud.pubsub_v1.SubscriberClient') as mock_client:
        yield mock_client

@pytest.fixture
def mock_transaction_repository():
    with mock.patch('Infrastructure.RepositoryKeeper.TransactionRepository') as mock_repo:
        instance = mock_repo.return_value
        instance.add_transaction_record = mock.Mock()
        yield instance

@pytest.fixture
def mock_logger():
    with mock.patch('loguru.logger') as mock_log:
        yield mock_log

@pytest.fixture
def mock_message():
    mock_msg = mock.Mock()
    mock_msg.data.decode = mock.Mock(return_value='Mocked message with data')
    mock_msg.ack = mock.Mock()
    yield mock_msg

# happy path - callback - Test that the callback function logs the received message.
def test_callback_logs_message(mock_logger, mock_message):
    callback(mock_message)
    mock_logger.debug.assert_called_with('Message received: Mocked message with data')


# happy path - callback - Test that the callback function decodes the message data correctly.
def test_callback_decodes_message_data(mock_message):
    callback(mock_message)
    mock_message.data.decode.assert_called_once()
    assert mock_message.data.decode() == 'Mocked message with data'


# happy path - callback - Test that the callback function acknowledges the message.
def test_callback_acknowledges_message(mock_message):
    callback(mock_message)
    mock_message.ack.assert_called_once()


# happy path - callback - Test that the callback function adds a transaction record.
def test_callback_adds_transaction_record(mock_transaction_repository, mock_message):
    callback(mock_message)
    mock_transaction_repository.add_transaction_record.assert_called_with('Mocked message with data')


# happy path - callback - Test that the callback function processes a valid message without exceptions.
def test_callback_processes_valid_message(mock_message):
    try:
        callback(mock_message)
        exception_raised = False
    except Exception:
        exception_raised = True
    assert not exception_raised


# edge case - callback - Test that the callback function handles a message with empty data gracefully.
def test_callback_handles_empty_message_data(mock_transaction_repository, mock_message):
    mock_message.data.decode.return_value = ''
    callback(mock_message)
    mock_transaction_repository.add_transaction_record.assert_called_with('')


# edge case - callback - Test that the callback function handles a message with non-UTF-8 data gracefully.
def test_callback_handles_non_utf8_data(mock_transaction_repository, mock_message):
    mock_message.data.decode.side_effect = UnicodeDecodeError('utf-8', b'', 0, 1, 'invalid start byte')
    try:
        callback(mock_message)
        exception_handled = True
    except UnicodeDecodeError:
        exception_handled = False
    assert exception_handled


# edge case - callback - Test that the callback function handles a message without an ack method gracefully.
def test_callback_handles_missing_ack_method(mock_message):
    del mock_message.ack
    try:
        callback(mock_message)
        exception_handled = True
    except AttributeError:
        exception_handled = False
    assert exception_handled


# edge case - callback - Test that the callback function handles an exception during transaction record addition.
def test_callback_handles_exception_in_transaction_record(mock_transaction_repository, mock_message):
    mock_transaction_repository.add_transaction_record.side_effect = Exception('Database error')
    try:
        callback(mock_message)
        exception_handled = True
    except Exception:
        exception_handled = False
    assert exception_handled


# edge case - callback - Test that the callback function does not process a message with invalid format.
def test_callback_handles_invalid_message_format(mock_transaction_repository, mock_message):
    mock_message.data.decode.return_value = None
    callback(mock_message)
    mock_transaction_repository.add_transaction_record.assert_not_called()


