import pytest
import json
from unittest.mock import patch, MagicMock
from anomaly_detection.worker import get_event_from_db, save_anomaly, process_event
from anomaly_detection.models.anomaly import Anomaly
from sqlalchemy.exc import OperationalError

# Sample event data
sample_event = {
    'request_id': 'req123',
    'event_id': 'evt456',
    'role_id': 'role789',
    'event_type': 'type1',
    'event_timestamp': '2023-01-01T00:00:00Z',
    'affected_assets': ['asset1', 'asset2'],
}


@pytest.fixture
def session_mock():
    return MagicMock()


@pytest.fixture
def mock_channel():
    channel = MagicMock()
    channel.basic_ack = MagicMock()
    return channel


@pytest.fixture
def mock_method():
    method = MagicMock()
    method.delivery_tag = 'mock_delivery_tag'
    return method


def test_get_event_from_db(session_mock):
    with patch('anomaly_detection.worker.transaction', lambda func: func):
        session_mock.query.return_value.filter_by.return_value.first.return_value = None
        event = get_event_from_db(session_mock, 'evt456')
        assert event is None


def test_save_anomaly(session_mock):
    with patch('anomaly_detection.worker.transaction', lambda func: func):
        save_anomaly(session_mock, sample_event)
        session_mock.add.assert_called_once()


def test_process_event_with_existing_event(mocker, session_mock, mock_channel, mock_method):
    with patch('anomaly_detection.worker.transaction', lambda func: func):
        mocker.patch('anomaly_detection.worker.get_event_from_db', return_value=Anomaly(**sample_event))
        mocker.patch('anomaly_detection.worker.save_anomaly')

        process_event(mock_channel, mock_method, None, json.dumps(sample_event))

        mock_channel.basic_ack.assert_called_once_with(delivery_tag='mock_delivery_tag')
        assert not save_anomaly.called


def test_process_event_with_new_anomaly(mocker, session_mock, mock_channel, mock_method):
    with patch('anomaly_detection.worker.transaction', lambda func: func):
        mocker.patch('anomaly_detection.worker.get_event_from_db', return_value=None)
        mocker.patch('anomaly_detection.worker.save_anomaly')

        process_event(mock_channel, mock_method, None, json.dumps(sample_event))

        mock_channel.basic_ack.assert_called_once_with(delivery_tag='mock_delivery_tag')
        save_anomaly.assert_called_once()
