from pydantic import BaseModel, EmailStr


class ReactivationRequest(BaseModel):
    email: EmailStr


class ReactivationConfirm(BaseModel):
    token: str
