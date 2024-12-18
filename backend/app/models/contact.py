from re import fullmatch

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
    validates,
)


from .base import Base


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
    phone_number: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        unique=True,
    )
    email: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )
    facebook: Mapped[Optional[str]] = mapped_column(
        String(30), nullable=True, default=None
    )
    vk: Mapped[Optional[str]] = mapped_column(String(30), nullable=True, default=None)

    client: Mapped["Client"] = relationship(back_populates="contacts")

    EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    PHONE_NUMBER_REGEX = r"^(\+?\d{1,2})?[-\s]?$?\d{3}$?[-\s]?\d{3}[-\s]?\d{4}$"

    @validates
    def validate_email(self, key, address):
        if not fullmatch(self.EMAIL_REGEX, address):
            raise ValueError(f"Некорректный адрес электронной почты: {address}")
        return address

    @validates
    def validate_phone_number(self, key, number):
        if not fullmatch(self.PHONE_NUMBER_REGEX, number):
            raise ValueError(f"Некорректный номер телефона: {number}")
        return number

    def __str__(self) -> str:
        """Возвращает строковое представление объекта."""
        return (
            f"{self.__class__.__name__}("
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
