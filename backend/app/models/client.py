from typing import (
    Optional,
    List,
    TYPE_CHECKING,
)
import datetime

from sqlalchemy import (
    String,
    Date,
)
from sqlalchemy.orm import (
    mapped_column,
    Mapped,
    relationship,
)

from .base import Base

if TYPE_CHECKING:
    from .contact import Contact


class Client(Base):
    """
    Класс для представления информации о клиенте.

    :param name: Имя клиента.
    :type name: str
    :param sur_name: Фамилия клиента.
    :type sur_name: str
    :param middle_name: Отчество клиента (необязательно).
    :type middle_name: Optional[str]
    :param cteate_at_day: Дата создания записи о клиенте.
    :type cteate_at_day: datetime.date
    :param updated_at_day: Дата последнего обновления записи о клиенте (необязательно).
    :type updated_at_day: Optional[datetime.date]
    """

    name: Mapped[str] = mapped_column(String(30), nullable=False)
    sur_name: Mapped[str] = mapped_column(String(30), nullable=False)
    middle_name: Mapped[Optional[str]] = mapped_column(
        String(30), nullable=True, default=None
    )
    cteate_at_day: Mapped[datetime.time] = mapped_column(Date, nullable=False)
    cteate_at_day: Mapped[Optional[datetime.time]] = mapped_column(
        Date, nullable=True, default=None
    )

    contacts: Mapped[List["Contact"]] = relationship(back_populates="client")
