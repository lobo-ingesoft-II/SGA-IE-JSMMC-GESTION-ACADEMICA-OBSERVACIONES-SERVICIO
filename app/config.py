from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    DEBUG: bool = Field(False, env="DEBUG")
    
    # URLs de otros microservicios
    ESTUDIANTES_API_URL: str = "http://sga-estudiantes-service:8005"
    AUTH_API_URL: str = "http://sga-sedes-service:8000"
    
    # Configuración de base de datos específica
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "observaciones_db"

    model_config = {"env_file": ".env"}
    
    @property
    def mysql_url(self) -> str:
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()