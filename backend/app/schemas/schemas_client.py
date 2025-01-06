from typing import (
    Optional,
    List,
    TYPE_CHECKING,
    Union
)

import datetime

from pydantic import BaseModel



from .schemas_contact import (
    ContactOut,
    ContactIn,
    ContactUpdate,
    )

class ClientBase(BaseModel):
    """
    Базовая модель клиента.

    Attributes:
        name (str): Имя клиента.
        sur_name (str): Фамилия клиента.
        middle_name (Optional[str]): Отчество клиента.
        contacts (ContactOut): Информация о контактах клиента
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
        sur_name (str): Фамилия клиента.
        middle_name (Optional[str]): Отчество клиента.
        create_at_day (datetime.datetime): Дата и время создания записи.
        update_at_day (Optional[datetime.datetime]): Дата и время последнего обновления записи.
        contacts (ContactOut): Информация о контактах клиента
    """

    id: int
    create_at_day: datetime.datetime
    update_at_day: Optional[datetime.datetime] = None

class ClientIn(ClientBase):
    """
    Модель для ввода информации о клиенте.

    Attributes:
        name (str): Имя клиента.
        sur_name (str): Фамилия клиента.
        middle_name (Optional[str]): Отчество клиента.
        contacts (ContactIn): Информация о контактах клиента
    """
    contacts: ContactIn


class ClientUpdate(ClientBase):
    name: Optional[str] = None
    sur_name: Optional[str] = None
    contacts: Union[ContactUpdate, None] = None


