from typing import List

from sqlalchemy import select,Result
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from models import Client, Contact

async def get_all_clients(
        session: AsyncSession,
) -> List[Client]:
    stmt = (select(Client, Contact).join(Contact, Client.id == Contact.client_id).options(joinedload(Client.contacts)))
    result: Result = await session.execute(stmt)
#     print(result.all())

    return result.scalars().all()
