from enum import Enum
from typing import Optional
from urllib.parse import quote_plus

from pydantic import BaseSettings, RedisDsn, validator


class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TEST = "test"


class BaseConfig(BaseSettings):
    class Config:
        case_sensitive = True


class Config(BaseConfig):
    DEBUG: int = 0
    DEFAULT_LOCALE: str = "en_US"
    ENVIRONMENT: str = EnvironmentType.DEVELOPMENT
    
    DB_SERVER: str = "localhost"
    DB_PORT: int = 1433
    DB_NAME_PRODUCTION: str = "fastapi_production_db"
    DB_NAME_TEST: str = "fastapi_test_db"
    DB_DRIVER: str = "ODBC Driver 17 for SQL Server"
    DB_TRUSTED_CONNECTION: str = "yes"
    DB_TRUST_SERVER_CERTIFICATE: str = "yes"
    DB_ENCRYPT: str = "yes"
    
    MSSQL_URL: Optional[str] = None
    MSSQL_URL_TEST: Optional[str] = None
    
    REDIS_URL: RedisDsn = "redis://localhost:6379/7"
    RELEASE_VERSION: str = "0.1"
    SHOW_SQL_ALCHEMY_QUERIES: int = 0
    SECRET_KEY: str = "super-secret-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24
    CELERY_BROKER_URL: str = "amqp://rabbit:password@localhost:5672"
    CELERY_BACKEND_URL: str = "redis://localhost:6379/0"

    @validator("MSSQL_URL", pre=True, always=True)
    def build_mssql_url(cls, v, values):
        if v:
            return v
        
        driver = quote_plus(values.get("DB_DRIVER", "ODBC Driver 18 for SQL Server"))
        server = values.get("DB_SERVER", "localhost")
        port = values.get("DB_PORT", 1433)
        database = values.get("DB_NAME_PRODUCTION", "fastapi_production_db")
        trusted_connection = values.get("DB_TRUSTED_CONNECTION", "yes")
        trust_server_certificate = values.get("DB_TRUST_SERVER_CERTIFICATE", "yes")
        encrypt = values.get("DB_ENCRYPT", "yes")
        
        connection_string = (
            f"DRIVER={{{values.get('DB_DRIVER')}}}"
            f";SERVER={server},{port}"
            f";DATABASE={database}"
            f";Trusted_Connection={trusted_connection}"
            f";TrustServerCertificate={trust_server_certificate}"
            f";Encrypt={encrypt}"
        )
        
        encoded_connection_string = quote_plus(connection_string)
        return f"mssql+aioodbc:///?odbc_connect={encoded_connection_string}"

    @validator("MSSQL_URL_TEST", pre=True, always=True)
    def build_mssql_url_test(cls, v, values):
        if v:
            return v
        
        driver = quote_plus(values.get("DB_DRIVER", "ODBC Driver 18 for SQL Server"))
        server = values.get("DB_SERVER", "localhost")
        port = values.get("DB_PORT", 1433)
        database = values.get("DB_NAME_TEST", "fastapi_test_db")
        trusted_connection = values.get("DB_TRUSTED_CONNECTION", "yes")
        trust_server_certificate = values.get("DB_TRUST_SERVER_CERTIFICATE", "yes")
        encrypt = values.get("DB_ENCRYPT", "yes")
        
        connection_string = (
            f"DRIVER={{{values.get('DB_DRIVER')}}}"
            f";SERVER={server},{port}"
            f";DATABASE={database}"
            f";Trusted_Connection={trusted_connection}"
            f";TrustServerCertificate={trust_server_certificate}"
            f";Encrypt={encrypt}"
        )
        
        encoded_connection_string = quote_plus(connection_string)
        return f"mssql+aioodbc:///?odbc_connect={encoded_connection_string}"

    @property
    def database_url(self) -> str:
        if self.ENVIRONMENT == EnvironmentType.TEST:
            return self.MSSQL_URL_TEST
        return self.MSSQL_URL


config: Config = Config()
