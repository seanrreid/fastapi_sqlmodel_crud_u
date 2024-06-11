from sqlmodel import Field, Relationship

from .base import Base


class Students(Base, table=True):
    __tablename__ = "students"

    name: str
