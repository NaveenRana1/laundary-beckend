from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud
import schema
from database import SessionalLocal

router = APIRouter()

def get_db():
    db = SessionalLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/bookings")
def create_booking(
    booking: schema.BookingCreate,
    db: Session = Depends(get_db)
):
    return crud.create_booking(db, booking)


@router.get("/bookings")
def get_all_bookings(
    db: Session = Depends(get_db)
):
    return crud.get_bookings(db)