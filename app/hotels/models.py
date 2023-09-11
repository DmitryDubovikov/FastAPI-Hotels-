from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    services = Column(JSON)
    number_of_rooms = Column(Integer, nullable=False)
    image_id = Column(Integer)

    # room = relationship("Rooms", back_populates="hotel")

    def __str__(self) -> str:
        return f"{self.name}"
