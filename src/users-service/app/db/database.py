from sqlmodel import Session, create_engine

from app.core.settings import settings


engine = create_engine(settings.DATABASE_URL, echo=False)


def get_session():
    """Dependency to get a database session."""
    with Session(engine) as session:
        yield session
