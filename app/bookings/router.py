from datetime import date

from fastapi import APIRouter, BackgroundTasks, Depends

# from pydantic import TypeAdapter

from app.bookings.dao import BookingDAO

from app.bookings.schemas import SBooking, SNewBooking

from app.exceptions import RoomCannotBeBookedException

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


@router.get("")
async def get_bookings(user: User = Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.fetch_all(user_id=user.id)


@router.post("")
async def create_booking(
    # background_tasks: BackgroundTasks,
    room_id: int,
    date_from: date,
    date_to: date,
    user: User = Depends(get_current_user),
):
    new_booking = await BookingDAO.insert(
        user_id=user.id, room_id=room_id, date_from=date_from, date_to=date_to
    )
    if not new_booking:
        raise RoomCannotBeBookedException

    # # celery
    # send_booking_confirmation.delay(
    #     {"date_from": new_booking.date_from, "date_to": new_booking.date_to}, user.email
    # )
    #
    # # background_tasks
    # background_tasks.add_task(
    #     send_booking_confirmation_with_background_tasks,
    #     {"date_from": new_booking.date_from, "date_to": new_booking.date_to},
    #     user.email,
    # )

    return new_booking


@router.delete("/{booking_id}")
async def remove_booking(
    booking_id: int,
    current_user: User = Depends(get_current_user),
):
    await BookingDAO.delete(id=booking_id, user_id=current_user.id)
