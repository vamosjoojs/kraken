from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from app.models.entities.base import BaseModel
from sqlalchemy.orm import relationship


class InstagramTasks(BaseModel):
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    use_same_db = Column(Boolean, default=False)
    use_same_db_instagram_handle = Column(String)
    instagram_handle = Column(String, nullable=False)
    activated = Column(Boolean, nullable=False, default=True)

    instagram_follow_id = Column(Integer, ForeignKey("instagram_follow.id"))
    instagram_follow = relationship("InstagramFollow", lazy="joined")
