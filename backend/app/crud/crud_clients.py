from typing import List
from datetime import datetime

from sqlalchemy import select, Result
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from models import Client, Contact

from schemas import (
    ClientOut,
    ClientIn,
)


async def fetch_all_clients(
    session: AsyncSession,
) -> List[ClientOut]:
    """Получает всех клиентов из базы данных.

    Args:
        session: Асинхронная сессия SQLAlchemy.

    Returns:
        Список объектов Client.
    """
    stmt = select(Client)
    result: Result = await session.execute(stmt)

    return result.scalars().all()


async def create_client_record(
    session: AsyncSession, new_client_data: ClientIn
) -> Client:
    """Создает запись о новом клиенте и связанные с ним контакты в базе данных.

    Args:
        session: Асинхронная сессия SQLAlchemy.
        new_client_data: Объект ClientIn, содержащий данные нового клиента.

    Returns:
        Объект Client, представляющий созданного клиента.

    """

    client = Client(
        name=new_client_data.name,
        sur_name=new_client_data.sur_name,
        middle_name=new_client_data.middle_name,
        create_at_day=datetime.now(),
    )

    session.add(client)
    await session.flush()
    contact = Contact(
        phone_number=new_client_data.contacts.phone_number,
        email=new_client_data.contacts.email,
        facebook=new_client_data.contacts.facebook,
        vk=new_client_data.contacts.vk,
        client_id=client.id,
    )

    session.add(contact)
    await session.commit()
    await session.refresh(client)

    return client
