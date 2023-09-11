from typing import List

from pydantic import BaseModel


class SHotel(BaseModel):
    id: int
    name: str
    location: str
    services: List[str]
    number_of_rooms: int
    image_id: int


class SHotelInfo(SHotel):
    rooms_left: int
