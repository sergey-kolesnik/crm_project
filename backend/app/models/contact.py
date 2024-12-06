from typing import (
    Optional,
    TYPE_CHECKING,
)

from sqlalchemy import (
    String,
    Integer,
    ForeignKey,
)

from sqlalchemy.orm import (
    mapped_column,
    Mapped,
    relationship,
)

from sqlalchemy_utils import (
    EmailType,
    PhoneNumberType,
)

from .base import Base
from .client import Client
if TYPE_CHECKING:
    from .client import Client


class Contact(Base):
    """
    Модель для хранения контактной информации клиента.

Attributes:
        id (int): Уникальный идентификатор контакта.
        client_id (int): Идентификатор клиента, которому принадлежит контакт.
        phone_number (sqlalchemy_utils.types.PhoneNumberType): Телефонный номер клиента.
        email (sqlalchemy_utils.types.EmailType): Адрес электронной почты клиента.
        facebook (Optional[str]): Ссылка на профиль клиента в Facebook (необязательное поле).
        vk (Optional[str]): Ссылка на профиль клиента в VK (необязательное поле).
        client (Client): Связь с объектом клиента
    """

    client_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("clients.id"), nullable=False
    )
    phone_number: Mapped[PhoneNumberType] = mapped_column(
        PhoneNumberType(),
        nullable=False,
        unique=True,
    )
    email: Mapped[EmailType] = mapped_column(
        EmailType,
        nullable=False,
        unique=True,
    )
    facebook: Mapped[Optional[str]] = mapped_column(
        String(30), nullable=True, default=None
    )
    vk: Mapped[Optional[str]] = mapped_column(String(30), nullable=True, default=None)

    client: Mapped[Client] = relationship(back_populates="contacts")

    def __str__(self) -> str:
        """Возвращает строковое представление объекта."""
        return (f"{self.__class__.__name__}("
        f"id={self.id},"
        f"client_id={self.client_id},"
        f"phone_number={self.phone_number},"
        f"email={self.email},"
        f"facebook={self.facebook!r},"
        f"vk={self.vk!r})"
        )

    def __repr__(self) -> str:
        """Возвращает строковое представление объекта для отображения в интерпретаторе."""
        return str(self)