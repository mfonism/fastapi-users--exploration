import uuid
from datetime import datetime

from pydantic import ConfigDict, EmailStr

from fastapi_users import schemas


class UserRead(schemas.CreateUpdateDictModel):
    id: uuid.UUID
    email: EmailStr
    is_superuser: bool = False
    deactivated_at: datetime | None = None
    verified_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class UserCreate(schemas.CreateUpdateDictModel):
    email: EmailStr
    password: str


class UserUpdate(schemas.CreateUpdateDictModel):
    password: str | None = None
    email: EmailStr | None = None
    deactivated_at: datetime | None = None
    verified_at: datetime | None = None
    is_superuser: bool | None = None

    def create_update_dict(self):
        # Keep regular users from mutating privileged/account-state fields.
        return self.model_dump(
            exclude_unset=True,
            exclude={"id", "is_superuser", "deactivated_at", "verified_at"},
        )
