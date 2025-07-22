from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Intentar usar DeclarativeBase (SQLAlchemy 2.0+) o declarative_base (SQLAlchemy 1.x)
try:
    from sqlalchemy.orm import DeclarativeBase
    
    class Base(DeclarativeBase):
        pass
except ImportError:
    # Fallback para SQLAlchemy 1.x
    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()

# Usar mysql_url en lugar de DATABASE_URL para evitar problemas
database_url = settings.mysql_url if settings.mysql_url else settings.DATABASE_URL
engine = create_engine(database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Connection successful:", result.scalar())
    except Exception as e:
        print("Connection failed:", e)