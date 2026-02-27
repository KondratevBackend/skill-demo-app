import pydantic
import pydantic_settings


class BaseSettings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(
        env_nested_delimiter="__", env_file=".env", use_enum_values=True, extra="ignore"
    )


class BotSettings(pydantic.BaseModel):
    token: str
    admins: list[int]
    support_url: pydantic.HttpUrl = pydantic.Field(default="https://t.me/privatka_support")


class ServerSettings(pydantic.BaseModel):
    username: str = pydantic.Field(default="admin")
    password: str = pydantic.Field(default="admin")


class DatabaseSettings(pydantic.BaseModel):
    dsn: pydantic.PostgresDsn
    engine_pool_size: int = pydantic.Field(default=20)
    engine_max_overflow: int = pydantic.Field(default=0)
    engine_pool_ping: bool = pydantic.Field(default=False)
    engine_pool_timeout: int = pydantic.Field(default=30)


class WorkerBrokerSettings(pydantic.BaseModel):
    dsn: pydantic.RedisDsn


class BotConfig(BaseSettings):
    bot: BotSettings
    database: DatabaseSettings
    server: ServerSettings


class WorkerConfig(BaseSettings):
    broker: WorkerBrokerSettings
    database: DatabaseSettings
    server: ServerSettings
