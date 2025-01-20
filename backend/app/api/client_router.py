from typing import (
    List,
    Annotated,
    )

from fastapi import (
    APIRouter, 
    Depends,
    HTTPException,
    status,
    )


from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.exc import IntegrityError

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
from core import (
    DatabaseError,
    UniqueViolationError,
    NotFoundError,
    crm_logger,
    )

router = APIRouter(
    prefix="/clients",
    tags=["clients"],
                   )


@router.get("/", response_model=List[ClientOut], tags=["clients"], status_code=200)
async def get_all_clients(
    session: Annotated[
        AsyncSession,
        Depends(db_async_session.session_get)
    ],
  ):
    """
    Получает всех клиентов из базы данных.
    
    Returns:
        List[ClientOut]: Список всех клиентов.

    Raises:
        DatabaseError: Если произошла ошибка при работе с базой данных.
    """
    try:
        all_clients = await fetch_all_clients(session=session)

        return all_clients
    except ConnectionRefusedError as error:
        crm_logger.error(f"Ошибка подключения к бд {error}")
        raise DatabaseError(detail="Ошибка сервера")
   
@router.post("/", tags=["clients"], response_model=ClientOut, status_code=201)
async def create_client(
    session: Annotated[AsyncSession, Depends(db_async_session.session_get)], 
                       data: ClientIn
):
    """
    Создает нового клиента в базе данных.

    Args:
        session: Асинхронная сессия SQLAlchemy.
        Данные нового клиента.

    Returns:
        ClientOut: Данные созданного клиента.

    Raises:
       UniqueViolationError: Если email клиента не уникальный.
        DatabaseError: Если произошла ошибка при работе с базой данных.
        Exception: Если произошла неизвестная ошибка.
    """
    try:
        new_client = await create_client_record(session=session, new_client_data=data)
        crm_logger.debug(f"Клиент создан успешно, id клиента: {new_client.id}")
        return new_client
    except ConnectionRefusedError as error:
      crm_logger.error(f"Ошибка подключения к бд {error}")
      raise DatabaseError(detail="Ошибка сервера")
    except IntegrityError as error:
        crm_logger.error(f"Ошибка при создании клиента, уникальное поле: {error}")
        raise UniqueViolationError(f"Ошибка при создании клиента, уникальное поле: {error}")



@router.patch("/{client_id}", tags=["clients"], status_code=200)
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
        NotFoundError: Если клиент с указанным ID не найден.
        UniqueViolationError: Если email клиента не уникальный.
        DatabaseError: Если произошла ошибка при работе с базой данных.

    """
    try:
        update_client = await update_client_record(session=session, new_client_data=data, client_id=client_id)
        crm_logger.debug(f"Клиент с id={client_id} успешно обновлён.")
        return update_client
    except ConnectionRefusedError as error:
        crm_logger.error(f"Ошибка подключения к бд {error}")
        raise DatabaseError(detail="Ошибка сервера")
    except ValueError as error:
        crm_logger.error(f"Ошибка при обновлении клиента {error}")
        raise NotFoundError(f"Клиент с id={client_id} не найден")
    except IntegrityError as error:
        crm_logger.error(f"Ошибка при обновлении клиента, уникальное поле: {error}")
        raise UniqueViolationError(f"Ошибка при обновлении клиента, уникальное поле: {error}")



@router.delete("/{client_id}", tags=["clients"], status_code=204)
async def delete_client(client_id: int, 
                        session: Annotated[AsyncSession, Depends(db_async_session.session_get)]):
    """
     Удаляет клиента из базы данных по ID.

    Args:
        client_id: ID клиента, которого нужно удалить.
        session: Асинхронная сессия SQLAlchemy.

    Returns:
        None: Возвращает пустой ответ с кодом 204.

    Raises:
       NotFoundError: Если клиент с указанным ID не найден.
       DatabaseError: Если произошла ошибка при работе с базой данных.
    """
    try:
        await delete_client_record(session=session, client_id=client_id)
        crm_logger.debug(f"Клиент с id={client_id} успешно удален")
    except ConnectionRefusedError as error:
        crm_logger.error(f"Ошибка подключения к бд {error}")
        raise DatabaseError(detail="Ошибка сервера")
    except ValueError as error:
        crm_logger.error(f"Ошибка при обновлении клиента {error}")
        raise NotFoundError(f"Клиент с id={client_id} не найден")
