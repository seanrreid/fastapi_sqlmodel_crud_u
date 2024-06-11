from sqlmodel import Field

from .base import Base


class Courses(Base, table=True):
    __tablename__ = "courses"

    name: str
