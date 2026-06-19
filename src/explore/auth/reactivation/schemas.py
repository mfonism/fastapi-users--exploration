from pydantic import BaseModel, EmailStr


class ReactivationRequest(BaseModel):
    email: EmailStr
