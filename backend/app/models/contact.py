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

if TYPE_CHECKING:
    from .client import Client


class Contact(Base):
    """
    Модель для хранения контактной информации клиента.

    :param client_id: Идентификатор клиента, которому принадлежит контакт.
    :type client_id: int
    :param phone_number: Телефонный номер клиента.
    :type phone_number: sqlalchemy_utils.types.PhoneNumberType
    :param email: Адрес электронной почты клиента.
    :type email: sqlalchemy_utils.types.EmailType
    :param facebook: Ссылка на профиль клиента в Facebook (необязательное поле).
    :type facebook: Optional[str]
    :param vk: Ссылка на профиль клиента в VK (необязательное поле).
    :type vk: Optional[str]
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
