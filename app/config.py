from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = ""
    SECRET_KEY: str = "your-secret-key-here"
    DEBUG: bool = False
    
    # URLs de otros microservicios
    ESTUDIANTES_API_URL: str = "http://localhost:8005"
    AUTH_API_URL: str = "http://localhost:8000"
    
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