from pydantic import BaseModel, EmailStr, field_validator
import re


class UserCreate(BaseModel):
    """Used by POST /register — name + email + password"""
    name: str
    email: EmailStr
    password: str

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be blank.")
        return v.strip()

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        errors = []
        if len(v) < 8:
            errors.append("at least 8 characters")
        if not re.search(r"[A-Z]", v):
            errors.append("one uppercase letter")
        if not re.search(r"[0-9]", v):
            errors.append("one number")
        if not re.search(r"[^A-Za-z0-9]", v):
            errors.append("one symbol")
        if errors:
            raise ValueError("Password must contain: " + ", ".join(errors) + ".")
        return v


class UserLogin(BaseModel):
    """Used by POST /login — email + password only"""
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True