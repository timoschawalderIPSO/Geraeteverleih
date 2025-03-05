from dataclasses import dataclass
import enum
from sqlalchemy import Boolean, Column, Enum, Integer, String
from sqlalchemy.orm import Mapped
from flask_login import UserMixin
from db.db import db

# Definition der Rollen
class Role(enum.Enum):
    Admin = 1
    Teacher = 2
    Student = 3

# Definition des Benutzermodells
@dataclass
class User(db.Model, UserMixin):
    __tablename__ = "user"

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String(256))
    email: Mapped[str] = Column(String(256), unique=True)
    password: Mapped[str] = Column(String(60))
    is_active: Mapped[bool] = Column(Boolean(), default=True)

    role: Mapped[Enum] = Column(Enum(Role))


