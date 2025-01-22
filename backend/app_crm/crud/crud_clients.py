from typing import List
from datetime import datetime, timezone

from sqlalchemy import select, Result

from sqlalchemy.ext.asyncio import AsyncSession

from models import Client, Contact

from schemas import (
    ClientOut,
    ClientIn,
    ClientUpdate,
)

from core import (
    DatabaseError,
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



async def update_client_record(session: AsyncSession,
                               client_id: int,
                               new_client_data: ClientUpdate):
    """Обновляет запись о клиенте и связанные с ним контакты в базе данных.

Args:
    session: Асинхронная сессия SQLAlchemy.
    client_id: ID клиента, данные которого нужно обновить.
    new_client_data: Объект ClientUpdate, содержащий новые данные клиента.

Returns:
        Объект Client, представляющий обновленного клиента.

Raises:
    ValueError: Если клиент с указанным ID не найден.
"""
    client = await session.get(Client, client_id)

    if not client:
        raise ValueError(f"Клиент с id {client_id} не найден")


    update_data = new_client_data.model_dump(exclude_none=True, exclude={"contacts"})
    update_data['update_at_day'] = datetime.now()

    for key, value in update_data.items():
        setattr(client, key, value)

    await session.commit()
    await session.refresh(client)

    if new_client_data.contacts:
        contact = await session.scalar(select(Contact).where(Contact.client_id == client_id))

        if contact:
            contact_data = new_client_data.contacts.model_dump(exclude_none=True)
            for key, value in contact_data.items():
                setattr(contact, key, value)
        session.add(contact)
    await session.commit()
    return client




async def delete_client_record(session: AsyncSession, client_id: int) -> None:
    client = await session.get(Client, client_id)

    if not client:
        raise ValueError(f"Клиент с id {client_id} не найден")
    
    await session.delete(client)
    await session.commit()


