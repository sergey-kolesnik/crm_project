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
    ClientIn,
    ClientUpdate,)

from crud import (fetch_all_clients, 
                  create_client_record, 
                  update_client_record,
                  delete_client_record,
                  )

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


@router.post("/", tags=["clients"], response_model=ClientOut)
async def create_client(
    session: Annotated[AsyncSession, Depends(db_async_session.session_get)], 
                       data: ClientIn
):
    new_client = await create_client_record(session=session, new_client_data=data)
    return new_client



@router.patch("/{client_id}")
async def update_client(
    client_id: int,
    session: Annotated[AsyncSession, Depends(db_async_session.session_get)],
    data: ClientUpdate,
):
    """Обновляет данные существующего клиента.

    Этот роут позволяет обновить информацию о клиенте по его ID.
    Принимает данные клиента в формате JSON в теле запроса.

    Args:
        client_id: ID клиента, данные которого нужно обновить.
        client_data: Объект ClientUpdate, содержащий новые данные клиента.
        session: Асинхронная сессия SQLAlchemy (Dependency).

    Returns:
        Объект ClientOut, содержащий обновленные данные клиента.

    Raises:
        HTTPException 404: Если клиент с указанным ID не найден.
        HTTPException 400: Если произошла ошибка при обновлении данных.
    """
    update_client = await update_client_record(session=session, new_client_data=data, client_id=client_id)
    return update_client


@router.delete("/{client_id}")
async def delete_client(client_id: int, 
                        session: Annotated[AsyncSession, Depends(db_async_session.session_get)]):
    
    await delete_client_record(session=session, client_id=client_id)
    return "ok"