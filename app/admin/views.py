from sqladmin import ModelView

from app.bookings.models import Booking
from app.hotels.models import Hotel
from app.hotels.rooms.models import Room
from app.users.models import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email]
    column_details_exclude_list = [User.hashed_password]
    can_delete = False
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"


class BookingAdmin(ModelView, model=Booking):
    column_list = [c.name for c in Booking.__table__.c] + [
        Booking.user,
        Booking.room,
    ]
    name = "Booking"
    name_plural = "Bookings"
    icon = "fa-solid fa-book"


class RoomAdmin(ModelView, model=Room):
    column_list = [c.name for c in Room.__table__.c] + [Room.hotel, Room.booking]
    name = "Room"
    name_plural = "Rooms"
    icon = "fa-solid fa-bed"


class HotelAdmin(ModelView, model=Hotel):
    column_list = [c.name for c in Hotel.__table__.c] + [Hotel.room]
    name = "Hotel"
    name_plural = "Hotels"
    icon = "fa-solid fa-hotel"
