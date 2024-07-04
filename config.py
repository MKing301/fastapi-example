from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    env_name: str
    base_url: str
    pg_user: str
    pg_pass: str
    pg_host: str
    pg_port: str
    pg_dbname: str

    class Config:
        env_file = ".env"


settings = Settings()
