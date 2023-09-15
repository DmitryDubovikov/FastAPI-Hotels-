from datetime import date, datetime, timedelta
from typing import List

from fastapi import APIRouter, Query

from app.hotels.rooms.dao import RoomDAO
from app.hotels.rooms.schemas import SRoom, SRoomInfo

router = APIRouter(prefix="/hotels", tags=["Rooms"])


@router.get("/{hotel_id}/rooms")
async def get_rooms_by_time(
    hotel_id: int,
    date_from: date = Query(..., description=f"For example, {datetime.now().date()}"),
    date_to: date = Query(
        ..., description=f"For example, {(datetime.now() + timedelta(days=14)).date()}"
    ),
) -> List[SRoomInfo]:
    rooms = await RoomDAO.fetch_all(hotel_id, date_from, date_to)
    return rooms
