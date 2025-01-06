
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    )


class ContactBase(BaseModel):
    """
    Базовый класс контакта.

    Attributes:
        phone_number (str): Номер телефона.
        email (str): Электронная почта.
        facebook (Optional[str]): Ссылка на профиль Facebook.
        vk (Optional[str]): Ссылка на профиль ВКонтакте.
    """

    phone_number: str
    email: str
    facebook: Optional[str] = None
    vk: Optional[str] = None

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class ContactOut(ContactBase):
    """
    Класс вывода данных контакта.

    Attributes:
        phone_number (str): Номер телефона.
        email (str): Электронная почта.
        facebook (Optional[str]): Ссылка на профиль Facebook.
        vk (Optional[str]): Ссылка на профиль ВКонтакте.
        client_id (int): id клиента.
    """
    client_id: int


class ContactIn(ContactBase):
    """
    Класс ввода данных контакта.

    Наследует все атрибуты от базового класса ContactBase.
    """
    pass



class ContactUpdate(ContactBase):
    phone_number: Optional[str] = None
    email: Optional[str] = None