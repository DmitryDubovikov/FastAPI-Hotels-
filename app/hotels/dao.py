from datetime import date

from sqlalchemy import and_, func, select

from app.bookings.models import Booking
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotel
from app.hotels.rooms.models import Room


class HotelDAO(BaseDAO):
    model = Hotel

    @classmethod
    async def fetch_all_by_location_and_time(
        cls, location: str, date_from: date, date_to: date
    ):
        """
        --only not booked

        WITH booked_rooms AS (
            SELECT room_id, COUNT(room_id) AS rooms_booked
            FROM bookings
            WHERE ('2023-10-05' > date_from and date_to > '2023-09-20')
            GROUP BY room_id
        ),
        booked_hotels AS (
            SELECT hotel_id, SUM(rooms.quantity - COALESCE(rooms_booked, 0)) AS rooms_left
            FROM rooms
            LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
            GROUP BY hotel_id
        )
        SELECT * FROM hotels
        LEFT JOIN booked_hotels ON booked_hotels.hotel_id = hotels.id
        WHERE rooms_left > 0 AND location LIKE '%Алтай%';
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

        booked_hotels = (
            select(
                Room.hotel_id,
                func.sum(
                    Room.quantity - func.coalesce(booked_rooms.c.rooms_booked, 0)
                ).label("rooms_left"),
            )
            .select_from(Room)
            .join(booked_rooms, booked_rooms.c.room_id == Room.id, isouter=True)
            .group_by(Room.hotel_id)
            .cte("booked_hotels")
        )

        get_hotels_with_rooms = (
            # Код ниже можно было бы расписать так:
            # select(
            #     Hotels
            #     booked_hotels.c.rooms_left,
            # )
            # Но используется конструкция Hotels.__table__.columns. Почему? Таким образом алхимия отдает
            # все столбцы по одному, как отдельный атрибут. Если передать всю модель Hotels и
            # один дополнительный столбец rooms_left, то будет проблематично для Pydantic распарсить
            # такую структуру данных. То есть проблема кроется именно в парсинге ответа алхимии
            # Пайдентиком.
            select(
                Hotel.__table__.columns,
                booked_hotels.c.rooms_left,
            )
            .join(booked_hotels, booked_hotels.c.hotel_id == Hotel.id, isouter=True)
            .where(
                and_(
                    booked_hotels.c.rooms_left > 0,
                    Hotel.location.like(f"%{location}%"),
                )
            )
        )
        async with async_session_maker() as session:
            # logger.debug(get_hotels_with_rooms.compile(engine, compile_kwargs={"literal_binds": True}))
            hotels_with_rooms = await session.execute(get_hotels_with_rooms)
            return hotels_with_rooms.mappings().all()
