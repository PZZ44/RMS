import sys
sys.path.append("/app")

from fastapi.testclient import TestClient
from unittest.mock import patch
from types import SimpleNamespace
from main import app

client = TestClient(app)


def valid_spr_payload():
    return {
        "id": 1,
        "client_id": "test-client",
        "first_name": "Тест",
        "last_name": "Тестов",
        "middle_name": "Тестович",
        "birth_date": "1995-01-01",
        "passport_number": "1234 567890",
        "phone_number": "79991112233",
        "loyal_client": 0,
        "successful_loans_count": 0,
        "requested_amount": 10000,
        "requested_days": 10,
    }


@patch("service.make_decision")   # 🔥 ВАЖНО: МОКАЕМ ИМЕННО ЭТУ ФУНКЦИЮ
def test_spr_decision_returns_valid_decision(mock_make_decision):

    mock_make_decision.return_value = (
        SimpleNamespace(
            id=1,
            decision="APPROVED",
            approved_amount=10000,
            approved_days=10,
        ),
        "APPROVED"
    )

    payload = valid_spr_payload()

    print("\n[TEST] POST /spr/decision")
    print("Payload:")
    print(payload)

    response = client.post("/spr/decision", json=payload)

    print("Status code:", response.status_code)
    print("Response body:")
    print(response.json())

    assert response.status_code == 200

    data = response.json()

    assert "decision" in data
    assert data["decision"] == "APPROVED"

    print("[OK] SPR decision =", data["decision"])
