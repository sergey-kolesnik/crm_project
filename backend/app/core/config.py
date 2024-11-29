from pydantic import (
    BaseModel,
    PostgresDsn,
    )

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class DataBaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = True
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

# 'postgresql+asyncpg',