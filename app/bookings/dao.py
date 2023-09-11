from datetime import date
from sqlalchemy import insert, select, and_, func

from app.bookings.models import Booking
from app.dao.base import BaseDAO
from app.hotels.rooms.models import Room
from app.database import engine, async_session_maker


class BookingDAO(BaseDAO):
    model = Booking
