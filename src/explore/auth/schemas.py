import uuid
from datetime import datetime

from fastapi_users import schemas
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRead(schemas.CreateUpdateDictModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str
    created_at: datetime
    updated_at: datetime
    last_login_at: datetime | None = None
    superuser_granted_at: datetime | None = None
    deactivated_at: datetime | None = None
    deleted_at: datetime | None = None
    verified_at: datetime | None = None
    terms_accepted_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CurrentUserRead(schemas.CreateUpdateDictModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserCreate(schemas.CreateUpdateDictModel):
    email: EmailStr
    full_name: str
    password: str = Field(json_schema_extra={"writeOnly": True})
    terms_accepted_at: datetime


class PasswordChange(BaseModel):
    current_password: str = Field(json_schema_extra={"writeOnly": True})
    new_password: str = Field(json_schema_extra={"writeOnly": True})


class EmailChangeRequest(BaseModel):
    new_email: EmailStr


class CurrentUserUpdate(schemas.CreateUpdateDictModel):
    full_name: str | None = None

    model_config = ConfigDict(extra="forbid")

    def create_update_dict(self):
        return self.model_dump(exclude_unset=True)
