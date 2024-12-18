from typing import List

from sqlalchemy import select,Result
from sqlalchemy.ext.asyncio import AsyncSession

from models import Client

async def get_all_clients(
        session: AsyncSession,
) -> List[Client]:
    stmt = select(Client).order_by(Client.id)
    result: Result = await session.scalars(stmt)
    return result.all()

