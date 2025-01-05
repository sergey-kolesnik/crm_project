from typing import (
    Optional,
    List,
    TYPE_CHECKING
)

import datetime

from pydantic import BaseModel



from .schemas_contact import (
    ContactOut,
    ContactIn,
    )

class ClientBase(BaseModel):
    """
    Базовая модель клиента.

    Attributes:
        name (str): Имя клиента.
        surname (str): Фамилия клиента.
        patronymic (Optional[str]): Отчество клиента.
        created_at (time): Дата и время создания записи.
        updated_at (Optional[time]): Дата и время последнего обновления записи.
        contacts (List[Contact]): Список контактов клиента.
    """

    name: str
    sur_name: str
    middle_name: Optional[str] = None
    
    contacts: ContactOut


    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class ClientOut(ClientBase):
    """
    Модель для вывода информации о клиенте.

    Attributes:
        id (int): Уникальный идентификатор клиента.
        name (str): Имя клиента.
        surname (str): Фамилия клиента.
        patronymic (Optional[str]): Отчество клиента.
        created_at (time): Дата и время создания записи.
        updated_at (Optional[time]): Дата и время последнего обновления записи.
        contacts (List[Contact]): Список контактов клиента.
    """

    id: int
    create_at_day: datetime.datetime
    update_at_day: Optional[datetime.datetime] = None

class ClientIn(ClientBase):
    contacts: ContactIn


