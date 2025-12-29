import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock
from auth import get_api_key, get_current_user


def test_get_api_key_no_header():
    with pytest.raises(HTTPException) as excinfo:
        get_api_key(None)
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "no authorization header included"


def test_get_api_key_malformed_header():
    # Wrong prefix
    with pytest.raises(HTTPException) as excinfo:
        get_api_key("Bearer token123")
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "malformed authorization header"

    # Missing parts
    with pytest.raises(HTTPException) as excinfo:
        get_api_key("ApiKey")
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "malformed authorization header"


def test_get_api_key_valid():
    api_key = get_api_key("ApiKey secret-key-123")
    assert api_key == "secret-key-123"


def test_get_current_user_found(monkeypatch):
    mock_db = MagicMock()
    mock_user = MagicMock()
    mock_user.id = "user1"

    # Mock crud.get_user_by_api_key
    mock_get_user = MagicMock(return_value=mock_user)
    monkeypatch.setattr("crud.get_user_by_api_key", mock_get_user)

    user = get_current_user(api_key="valid-key", db=mock_db)

    assert user == mock_user
    mock_get_user.assert_called_once_with(mock_db, "valid-key")


def test_get_current_user_not_found(monkeypatch):
    mock_db = MagicMock()

    # Mock crud.get_user_by_api_key to return None
    mock_get_user = MagicMock(return_value=None)
    monkeypatch.setattr("crud.get_user_by_api_key", mock_get_user)

    with pytest.raises(HTTPException) as excinfo:
        get_current_user(api_key="invalid-key", db=mock_db)

    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Couldn't get user"
