from sqlalchemy.orm import Session
from model import User, Booking
import schema, model
from schema import UserCreate, BookingCreate
from auth import hash_password

def ger_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: UserCreate):
    new_user = User(
        username=user.username,
        password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

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