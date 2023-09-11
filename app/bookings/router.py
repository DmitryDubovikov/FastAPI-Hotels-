from datetime import date

from fastapi import APIRouter, BackgroundTasks, Depends

# from pydantic import TypeAdapter

from app.bookings.dao import BookingDAO

from app.bookings.schemas import SBooking, SNewBooking

# from app.exceptions import RoomCannotBeBookedException
# from app.tasks.tasks import (
#     send_booking_confirmation,
#     send_booking_confirmation_with_background_tasks,
# )
from app.users.dependencies import get_current_user
from app.users.models import User

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("/all")
async def get_bookings() -> list[SBooking]:
    # TODO: только для тестирования. в финале удалить
    return await BookingDAO.fetch_all()


@router.get("/")
async def get_bookings(user: User = Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.fetch_all(user_id=user.id)
