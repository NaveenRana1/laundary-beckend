from sqlalchemy.orm import Session
from model import User, Booking
import schema, model
from schema import UserCreate
from auth import hash_password


def create_booking(db: Session, booking: schema.BookingCreate):

    db_booking = model.Booking(
        name=booking.name,
        phone=booking.phone,
        address=booking.address,
        service=booking.service,
        date=booking.date,
        notes=booking.notes,
        quantity=booking.quantity
    )

    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)

    return db_booking


def get_bookings(db: Session):
    return db.query(model.Booking).all()