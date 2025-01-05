from typing import (
    Optional,
    List,
    TYPE_CHECKING,
)
import datetime

from sqlalchemy import (
    String,
    DateTime,
    func,
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

    Attributes:
        id (int): Уникальный идентификатор клиента.
        name (str): Имя клиента.
        sur_name (str): Фамилия клиента.
        middle_name (Optional[str]): Отчество клиента (необязательно).
        create_at_day (datetime.date): Дата создания записи о клиенте.
        update_at_day (Optional[datetime.date]): Дата последнего обновления записи о клиенте (необязательно).
        contacts (List['Contact']): Список контактов клиента
    """

    name: Mapped[str] = mapped_column(String(30), nullable=False)
    sur_name: Mapped[str] = mapped_column(String(30), nullable=False)
    middle_name: Mapped[Optional[str]] = mapped_column(
        String(30), nullable=True, default=None
    )
    create_at_day: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    update_at_day: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)

    contacts: Mapped["Contact"] = relationship(back_populates="client",  uselist=False, lazy="joined")

    def __str__(self) -> str:
        """Возвращает строковое представление объекта."""
        return (
            f"{self.__class__.__name__}("
            f"id={self.id},"
            f"name={self.name!r},"
            f"sur_name={self.sur_name!r},"
            f"middle_name={self.middle_name!r},"
            f"create_at_day={self.create_at_day!r},"
            f"update_at_day={self.update_at_day!r})"
        )

    def __repr__(self) -> str:
        """Возвращает строковое представление объекта для отображения в интерпретаторе."""
        return str(self)
    
