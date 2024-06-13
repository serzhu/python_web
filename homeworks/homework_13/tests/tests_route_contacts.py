
from unittest.mock import AsyncMock, patch
import pytest
from fastapi import status
from src.services.auth import auth_service

def test_create_contact(client, get_token, monkeypatch):
    with patch.object(auth_service, 'cache') as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        
        contact = {
            "name": "John",
            "surname": "John",
            "email": "john@example.com",
            "phone": "+380954703544",
            "birthday": "2024-06-15",
            "info": "Friend"
        }

        response = client.post("api/contacts", json=contact, headers=headers)
        assert response.status_code == status.HTTP_201_CREATED,  f"Expected status code 201, got {response.status_code}"
        response_json = response.json()
        assert response.json()["name"] == "John", f"Expected contact name 'John', got {response_json['name']}"


def test_get_contacts(client, get_token, monkeypatch):
    with patch.object(auth_service, 'cache') as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get("api/contacts", headers=headers)
        assert response.status_code == status.HTTP_200_OK, f"Expected status code 200, got {response.status_code}"
        response_json = response.json()
        assert isinstance(response_json, list), "Expected response to be a list"
        assert len(response_json) == 1, "Expected at least one contact in the response"
        first_contact = response_json[0]
        assert first_contact["name"] == "John", f"Expected first contact name 'John', got {first_contact['name']}"


def test_get_all_contacts(client, get_token, monkeypatch):
    with patch.object(auth_service, 'cache') as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get("api/contacts/all", headers=headers)
        assert response.status_code == status.HTTP_200_OK, f"Expected status code 200, got {response.status_code}"
        response_json = response.json()
        assert isinstance(response_json, list), "Expected response to be a list"
        assert len(response_json) == 1, "Expected at least one contact in the response"
        first_contact = response_json[0]
        assert first_contact["name"] == "John", f"Expected first contact name 'John', got {first_contact['name']}"


def test_get_contact(client, get_token, monkeypatch):
    with patch.object(auth_service, 'cache') as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get("api/contacts/1", headers=headers)
        assert response.status_code == status.HTTP_200_OK, f"Expected status code 200, got {response.status_code}"
        response_json = response.json()
        assert isinstance(response_json, dict), "Expected response to be a dict"
        assert response_json["name"] == "John", f"Expected first contact name 'John', got {response_json['name']}"

        response = client.get("api/contacts/2", headers=headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND, f"Expected status code 404, got {response.status_code}"


def test_find_contact(client, get_token, monkeypatch):
    with patch.object(auth_service, 'cache') as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        
        find_str = "John"
        response = client.get(f"api/contacts/find/?find_str={find_str}", headers=headers)
        assert response.status_code == status.HTTP_200_OK, f"Expected status code 200, got {response.status_code}"
        response_json = response.json()
        assert isinstance(response_json, list), "Expected response to be a list"
        assert len(response_json) == 1, "Expected at least one contact in the response"
        first_contact = response_json[0]
        assert first_contact["name"] == "John", f"Expected first contact name 'John', got {first_contact['name']}"
        
        find_str = "Alex"
        response = client.get(f"api/contacts/find/?find_str={find_str}", headers=headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND, f"Expected status code 404, got {response.status_code}"


def test_find_next_days_birthdays(client, get_token, monkeypatch):
    with patch.object(auth_service, 'cache') as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        
        next_days = 7
        response = client.get(f"api/contacts/next_days_birthdays/?next_days={next_days}", headers=headers)
        assert response.status_code == status.HTTP_200_OK, f"Expected status code 200, got {response.status_code}"
        response_json = response.json()
        assert isinstance(response_json, list), "Expected response to be a list"
        assert len(response_json) == 1, "Expected at least one contact in the response"
        first_contact = response_json[0]
        assert first_contact["name"] == "John", f"Expected first contact name 'John', got {first_contact['name']}"

        next_days = 1
        response = client.get(f"api/contacts/next_days_birthdays/?next_days={next_days}", headers=headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND, f"Expected status code 404, got {response.status_code}"


def test_update_contact(client, get_token, monkeypatch):
    with patch.object(auth_service, 'cache') as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}

        update_contact = {
            "name": "Alex",
            "surname": "Alex",
            "email": "alex@example.com",
            "phone": "+380954703544",
            "birthday": "2024-06-12",
            "info": "Friend"
        }

        response = client.put(f"api/contacts/1", json=update_contact, headers=headers)
        assert response.status_code == status.HTTP_200_OK, f"Expected status code 200, got {response.status_code}"
        updated_contact =  response.json()
        assert updated_contact["name"] == "Alex", f"Expected contact name 'Alex', got {updated_contact['name']}"

        response = client.put(f"api/contacts/2", json=update_contact, headers=headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND, f"Expected status code 404, got {response.status_code}"


def test_delete_contact(client, get_token, monkeypatch):
    with patch.object(auth_service, 'cache') as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}

        response = client.delete(f"api/contacts/1", headers=headers)
        assert response.status_code == status.HTTP_200_OK, f"Expected status code 200, got {response.status_code}"

        response = client.delete(f"api/contacts/1", headers=headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND, f"Expected status code 404, got {response.status_code}"
