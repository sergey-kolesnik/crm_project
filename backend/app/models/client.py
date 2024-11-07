from typing import Optional
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

class Client(Base):
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    sur_name: Mapped[str] = mapped_column(String(30), nullable=False)
    middle_name: Mapped[Optional[str]] = mapped_column(String(30), nullable=True, default=None)
    cteate_at_day: Mapped[datetime.time] = mapped_column(Date, nullable=False)
    cteate_at_day: Mapped[Optional[datetime.time]] = mapped_column(Date, nullable=True, default=None)

