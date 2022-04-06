from __future__ import annotations
from sqlalchemy.orm import Session


class UnitOfWork:
    def __init__(self, session: Session):
        self.session = session

    def __enter__(self) -> UnitOfWork:
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type:
            self.rollback()
        else:
            self.commit()

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()
