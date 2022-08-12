from sqlalchemy import Column, Integer, String, Boolean
from app.models.entities.base import BaseModel


class Parameters(BaseModel):
    name = Column(String, nullable=False)
    activated = Column(Boolean, nullable=False)
    value = Column(String)
    bool_value = Column(Boolean)
    int_value = Column(Integer)
