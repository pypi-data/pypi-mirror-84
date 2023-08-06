import pytest
import requests
import requests_mock

from postbode.client import Client

mock_api_token = '123456789qwerty'
mock_client = Client(mock_api_token)
mock_mailboxes = {
    "id": 15,
    "name": "John Doe Mailbox",  # Mailbox name
    "vat_shifted": 0,
    "webhook_url": "",
    "balance": 0,
}


def test_client_url():
    assert mock_client.api_base_url == 'https://app.postbode.nu/api'


def test_client_header():
    assert mock_client.headers['Content-Type'] == 'application/json'


def test_client_header_token():
    assert mock_client.headers['X-Authorization'] == mock_api_token


def test_get_mailboxes(requests_mock):
    requ = requests_mock.get(
        'https://app.postbode.nu/api/mailbox', json=mock_mailboxes)
    resp = mock_client.get_mailboxes()
    assert resp == mock_mailboxes
