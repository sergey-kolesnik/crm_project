from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
)

from core import settings


class DataBaseConnect:
    """Класс для управления подключениями к базе данных.

    Этот класс обеспечивает создание и управление асинхронными соединениями с базой данных.
    Он использует движок SQLAlchemy для создания и настройки соединений.

    Attributes:
        engine (AsyncEngine): Асинхронный движок базы данных.
        session_factory (async_sessionmaker[AsyncSession]): Фабрика сессий для создания асинхронных сессий.
    """

    def __init__(
        self,
        url: str,
        echo: bool = True,
        echo_pool: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
    ) -> None:
        """Инициализация класса DataBaseConnect.

        Attributes:
            url (str): URL подключения к базе данных.
            echo (bool, optional): Включает логирование SQL-запросов. По умолчанию: True.
            echo_pool (bool, optional): Включает логирование событий пула соединений. По умолчанию: False.
            pool_size (int, optional): Размер пула соединений. По умолчанию: 5.
            max_overflow (int, optional): Максимальное количество дополнительных соединений сверх размера пула. По умолчанию: 10.
        """
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )

        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        """Освобождение ресурсов, связанных с двигателем базы данных.

        Данный метод завершает все активные соединения и освобождает ресурсы, используемые движком базы данных.
        """
        if self.engine:
            await self.engine.dispose()

    async def session_get(self) -> AsyncGenerator[AsyncSession, None]:
        """Получение асинхронной сессии из фабрики сессий.

        Метод создает и возвращает асинхронную сессию, используя фабрику сессий.

        Yields:
            AsyncSession: Асинхронная сессия базы данных."""
        async with self.session_factory() as session:
            yield session


db_async_session = DataBaseConnect(
    url=str(settings.db.url),
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow

)
