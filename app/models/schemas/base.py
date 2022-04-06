import pydantic


class Base(pydantic.BaseModel):
    class Config:
        orm_mode = True
