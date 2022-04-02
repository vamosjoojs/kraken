from sqlalchemy import Column, Integer, String, Boolean
from app.models.entities.base import BaseModel


class Parameters(BaseModel):
    name = Column(String, nullable=False)
    activated = Column(Boolean, nullable=False)
    value = Column(String, nullable=False)
    bool_value = Column(Boolean, nullable=False)
    int_value = Column(Integer, nullable=False)
