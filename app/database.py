from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Carrega variáveis do .env
load_dotenv()

# Variáveis de ambiente
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")

# URL de conexão
DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

# Engine com pool configurado
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)

# SessionLocal -> cada request cria uma sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base -> usada para declarar os models
Base = declarative_base()

# Dependency para injetar sessão nos routers
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
