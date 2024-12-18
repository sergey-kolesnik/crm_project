from typing import (
    List,
    Annotated,
    )

from fastapi import (
    APIRouter, 
    Depends
    )

from sqlalchemy.ext.asyncio import AsyncSession

from schemas import ClientOutput

from crud import get_all_clients

from models import db_async_session

router = APIRouter(
    prefix="/clients",
                   )


@router.get("/", response_model=List[ClientOutput])
async def get_clients(
    session: Annotated[
        AsyncSession,
        Depends(db_async_session.session_get)
    ],
):
    clients = await get_all_clients(session=session)
    return clients
