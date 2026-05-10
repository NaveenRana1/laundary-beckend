from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"

    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String, nullable=False)
    email      = Column(String, unique=True, index=True, nullable=False)
    password   = Column(String, nullable=False)       # bcrypt hash
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Booking(Base):
    __tablename__ = "bookings"

    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String, nullable=False)
    email      = Column(String, nullable=False)
    phone      = Column(String, nullable=False)
    address    = Column(String, default="")
    service    = Column(String, nullable=False)
    date       = Column(String, default="")
    notes      = Column(String, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())