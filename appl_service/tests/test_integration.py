from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def valid_payload():
    return {
        "first_name": "Иван",
        "last_name": "Иванов",
        "middle_name": "Иванович",
        "birth_date": "1995-01-01",
        "passport_number": "1234 567890",
        "phone_number": "79990001122",
        "requested_amount": 10000,
        "requested_days": 10,
    }


def test_create_application_success():
    payload = valid_payload()

    print("\n[TEST] Создание заявки /applications")
    print("Отправляемый payload:")
    print(payload)

    response = client.post("/applications", json=payload)

    print("Статус ответа:", response.status_code)
    print("Тело ответа:")
    print(response.json())

    assert response.status_code == 200

    body = response.json()
    assert "id" in body
    assert "decision" in body
    assert body["requested_amount"] == 10000
    assert body["requested_days"] == 10

    print("[OK] Заявка успешно создана")


def test_create_application_validation_error():
    bad_payload = valid_payload()
    del bad_payload["passport_number"]

    print("\n[TEST] Ошибка валидации /applications")
    print("Отправляемый payload (некорректный):")
    print(bad_payload)

    response = client.post("/applications", json=bad_payload)

    print("Статус ответа:", response.status_code)
    print("Тело ответа:")
    print(response.json())

    assert response.status_code == 422

    print("[OK] Ошибка валидации обработана корректно")
