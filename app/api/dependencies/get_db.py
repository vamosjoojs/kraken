from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.config import config

engine = create_engine(config.DATABASE_URI_ASYNC, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_uow():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
