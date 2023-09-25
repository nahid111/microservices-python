from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

db_user = settings.MYSQL_USER
db_pass = settings.MYSQL_PASSWORD
db_host = settings.MYSQL_HOST
db_port = settings.MYSQL_PORT
db_name = settings.MYSQL_DATABASE

SQLALCHEMY_DATABASE_URL = f"mysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
