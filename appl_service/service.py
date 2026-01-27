import uuid
from sqlalchemy.orm import Session
from models import Application


# можно вынести в константы
CLIENT_NAMESPACE = uuid.UUID("12345678-1234-5678-1234-567812345678")


def create_application(
    db: Session,
    data
):
    """
    Создаёт заявку:
    - генерирует стабильный client_id (UUID5)
    - сохраняет заявку в БД
    """

    # детерминированная строка идентификации клиента
    identity_string = f"{data.phone_number}|{data.first_name}|{data.birth_date}|{data.passport_number}"

    # стабильный UUID
    client_id = str(uuid.uuid5(CLIENT_NAMESPACE, identity_string))

    application = Application(
        client_id=client_id,
        last_name=data.last_name,
        first_name=data.first_name,
        middle_name=data.middle_name,
        birth_date=data.birth_date,
        passport_number=data.passport_number,
        phone_number=data.phone_number,
        requested_amount=data.requested_amount,
        requested_days=data.requested_days,
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return application
