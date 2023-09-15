from datetime import date

from sqlalchemy import and_, func, insert, select
from sqlalchemy.exc import SQLAlchemyError

from app.bookings.models import Booking
from app.dao.base import BaseDAO
from app.database import async_session_maker, engine
from app.hotels.rooms.models import Room
from app.logger import logger
from app.exceptions import RoomIsFullyBooked


class BookingDAO(BaseDAO):
    model = Booking

    @classmethod
    async def insert(cls, user_id: int, room_id: int, date_from: date, date_to: date):
        # query available rooms
        """
        with booked_rooms as (
            select * from bookings
            where room_id = 5 and ('2023-09-27' > bookings.date_from and bookings.date_to > '2023-09-20'
        )
        select rooms.quantity - COUNT(booked_rooms.room_id) from rooms
        left join booked_rooms on booked_rooms.room_id = rooms.id
        where rooms.id = 5
        group by rooms.quantity, booked_rooms.room_id
        """
        try:
            async with async_session_maker() as session:
                booked_rooms = (
                    select(Booking)
                    .where(
                        and_(
                            Booking.room_id == room_id,
                            date_to > Booking.date_from,
                            Booking.date_to > date_from,
                        )
                    )
                    .cte("booked_rooms")
                )
                rooms_left = (
                    (
                        select(
                            (Room.quantity - func.count(booked_rooms.c.room_id)).label(
                                "rooms_left"
                            )
                        )
                        .select_from(Room)
                        .join(
                            booked_rooms,
                            booked_rooms.c.room_id == Room.id,
                            isouter=True,
                        )
                    )
                    .where(Room.id == room_id)
                    .group_by(Room.quantity, booked_rooms.c.room_id)
                )

                # print(rooms_left.compile(engine, compile_kwargs={"literal_binds": True}))

                rooms_left = await session.execute(rooms_left)
                number_rooms_left: int = rooms_left.scalar()

                if number_rooms_left == 0:
                    extra = {
                        "user_id": user_id,
                        "room_id": room_id,
                        "date_from": date_from,
                        "date_to": date_to,
                    }
                    logger.info("RoomIsFullyBooked", extra=extra, exc_info=True)
                    raise RoomIsFullyBooked
                get_price = select(Room.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()

                insert_booking = (
                    insert(Booking)
                    .values(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=price,
                    )
                    .returning(Booking)
                )
                new_booking = await session.execute(insert_booking)
                await session.commit()
                return new_booking.scalar()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot add booking"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot add booking"
            extra = {
                "user_id": user_id,
                "room_id": room_id,
                "date_from": date_from,
                "date_to": date_to,
            }
            logger.error(msg, extra=extra, exc_info=True)
