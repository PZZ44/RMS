from fastapi.testclient import TestClient
from unittest.mock import patch
from types import SimpleNamespace
import datetime

from main import app

client = TestClient(app)


def valid_payload():
    return {
        "first_name": "Тест",
        "last_name": "Тестов",
        "middle_name": "Тестович",
        "birth_date": "1995-01-01",
        "passport_number": "1234 567890",
        "phone_number": "79991112233",
        "requested_amount": 10000,
        "requested_days": 10,
    }


@patch("service.create_application")
@patch("clients.call_spr")
def test_create_application_success(mock_call_spr, mock_create):
    mock_create.return_value = SimpleNamespace(
        id=1,
        client_id="test-client-id",
        first_name="Тест",
        last_name="Тестов",
        middle_name="Тестович",
        birth_date=datetime.date(1995, 1, 1), 
        passport_number="1234 567890",
        phone_number="79991112233",
        requested_amount=10000,
        requested_days=10,
    )

    mock_call_spr.return_value = {
        "decision": "APPROVED",
        "approved_amount": 10000,
        "approved_days": 10,
    }

    payload = valid_payload()

    print("Отправка POST /applications")
    print("Payload:")
    print(payload)

    response = client.post("/applications", json=payload)

    print("Статус ответа:", response.status_code)
    print("Тело ответа:")
    print(response.json())


    assert response.status_code == 200

    body = response.json()
    assert body["id"] == 1
    assert body["decision"] == "APPROVED"
