from pydantic import BaseModel, EmailStr, Field


class EmailChangeRequest(BaseModel):
    new_email: EmailStr


class EmailChangeConfirm(BaseModel):
    token: str = Field(json_schema_extra={"writeOnly": True})
