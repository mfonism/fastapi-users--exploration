import uuid
from datetime import datetime

from fastapi_users import schemas
from pydantic import ConfigDict, EmailStr, Field

from .email_identity import normalize_email


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


class UserCreate(schemas.CreateUpdateDictModel):
    email: EmailStr
    full_name: str
    password: str = Field(json_schema_extra={"writeOnly": True})
    terms_accepted_at: datetime

    def create_update_dict(self):
        user_dict = super().create_update_dict()
        user_dict["email"] = normalize_email(user_dict["email"])
        return user_dict
