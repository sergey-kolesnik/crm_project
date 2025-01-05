from typing import (
    List,
    Annotated,
    )

from fastapi import (
    APIRouter, 
    Depends,
    Form,
    )

from sqlalchemy.ext.asyncio import AsyncSession

from schemas import (
    ClientOut,
    ClientIn)

from crud import fetch_all_clients, create_client_record

from db_connection_async import db_async_session

router = APIRouter(
    prefix="/clients",
    tags=["clients"],
                   )


@router.get("/", response_model=List[ClientOut], tags=["clients"])
async def get_all_clients(
    session: Annotated[
        AsyncSession,
        Depends(db_async_session.session_get)
    ],
  ):
    all_clients = await fetch_all_clients(session=session)

    return all_clients


@router.post("/", tags=["clients"])
async def create_client(
    session: Annotated[AsyncSession, Depends(db_async_session.session_get)], 
                       data: ClientIn
):
    new_client = await create_client_record(session=session, new_client_data=data)
    return new_client
