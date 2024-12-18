
from typing import Optional

from pydantic import BaseModel


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
    facebook: Optional[str]
    vk: Optional[str]


class ContactOutput(ContactBase):
    """Класс вывода данных контакта.

Наследует все атрибуты от базового класса ContactBase.
"""
    pass