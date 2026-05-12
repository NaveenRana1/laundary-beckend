from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

import routes
import model
import schema

from database import Base, engine
from routes import get_db
from auth import verify_password, hash_password, create_token

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# ✅ CORS must be FIRST
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(routes.router)


# ------------------------
# Helper functions
# ------------------------
def get_user_by_email(db: Session, email: str):
    return db.query(model.User).filter(model.User.email == email).first()


def create_user(db: Session, user: schema.UserCreate):
    new_user = model.User(
        name=user.name,
        email=user.email.lower(),
        password=hash_password(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# ------------------------
# API endpoints
# ------------------------
@app.get("/")
def home():
    return {"message": "backend is running"}


@app.post("/register")
def register(user: schema.UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, user.email.lower())

    if existing:
        raise HTTPException(status_code=400, detail="Email is already registered.")

    create_user(db, user)

    return {"message": "User created successfully"}


@app.post("/login")
def login(user: schema.UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email.lower())

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    token = create_token({"sub": db_user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }