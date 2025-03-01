from dataclasses import dataclass
from db.db import db
from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped



@dataclass
class Device(db.Model):
    __tablename__ = "device"

    id: Mapped[int] = Column(Integer, primary_key=True)
    device_name: Mapped[str] = Column(String(256))
    device_type: Mapped[str] = Column(String(256))
    description: Mapped[str] = Column(String(4096))
    is_available: Mapped[bool] = Column(Boolean(), default=True)

    user = db.relationship("User", backref='devices')
    user_id: Mapped[int] = Column(Integer, ForeignKey('user.id'))

    def to_dict(self):
        return {
            "id": self.id,
            "device_name": self.device_name,
            "device_type": self.device_type,
            "description": self.description,
            "is_available": self.is_available,
            "user_id": self.user_id
        }



