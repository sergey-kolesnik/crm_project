from pydantic import BaseModel, PostgresDsn

from dotenv import load_dotenv


from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

load_dotenv()


class DataBaseConfig(BaseModel):
    """Конфигурация подключения к базе данных PostgreSQL.

    Attributes:
        url (PostgresDsn): URL подключения к базе данных.
        echo (bool): Флаг, определяющий необходимость вывода SQL-запросов в консоль. По умолчанию: True.
        echo_pool (bool): Флаг, определяющий необходимость вывода информации о пуле соединений. По умолчанию: False.
        pool_size (int): Размер пула соединений. По умолчанию: 50.
        max_overflow (int): Максимальное количество дополнительных соединений сверх размера пула. По умолчанию: 10.
    """

    url: PostgresDsn
    echo: bool = True
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class Settings(BaseSettings):
    """Класс настроек приложения.

    Этот класс используется для загрузки и управления настройками приложения.
    Настройки могут быть загружены из файла .env или переданы через переменные окружения.

    Attributes:
        model_config (SettingsConfigDict): Конфигурация модели настроек.
            Определяет файл конфигурации (.env), а также чувствительность к регистру имен параметров.
        db (DataBaseConfig): Конфигурация подключения к базе данных.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        extra="ignore",
    )

    db: DataBaseConfig


settings = Settings()

