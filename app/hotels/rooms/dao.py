from app.database import async_session_maker
from app.dao.base import BaseDAO
from app.hotels.rooms.models import Room
from app.bookings.models import Booking
from datetime import date
from sqlalchemy import and_, func, or_, select


class RoomDAO(BaseDAO):
    model = Room

    @classmethod
    async def fetch_all(cls, hotel_id: int, date_from: date, date_to: date):
        """
        WITH booked_rooms AS (
            SELECT room_id, COUNT(room_id) AS rooms_booked
            FROM bookings
            WHERE ('2023-10-05' > date_from and date_to > '2023-09-20')
            GROUP BY room_id
        )
        SELECT
            -- все столбцы из rooms,
            (quantity - COALESCE(rooms_booked, 0)) AS rooms_left FROM rooms
        LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        WHERE hotel_id = 1
        """
        booked_rooms = (
            select(Booking.room_id, func.count(Booking.room_id).label("rooms_booked"))
            .select_from(Booking)
            .where(
                and_(
                    date_to > Booking.date_from,
                    Booking.date_to > date_from,
                )
            )
            .group_by(Booking.room_id)
            .cte("booked_rooms")
        )

        get_rooms = (
            select(
                Room.__table__.columns,
                (Room.price * (date_to - date_from).days).label("total_cost"),
                (Room.quantity - func.coalesce(booked_rooms.c.rooms_booked, 0)).label(
                    "rooms_left"
                ),
            )
            .join(booked_rooms, booked_rooms.c.room_id == Room.id, isouter=True)
            .where(Room.hotel_id == hotel_id)
        )
        async with async_session_maker() as session:
            # logger.debug(get_rooms.compile(engine, compile_kwargs={"literal_binds": True}))
            rooms = await session.execute(get_rooms)
            return rooms.mappings().all()
