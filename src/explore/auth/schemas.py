import uuid
from datetime import datetime

from pydantic import ConfigDict, EmailStr

from fastapi_users import schemas


class UserRead(schemas.CreateUpdateDictModel):
    id: uuid.UUID
    email: EmailStr
    superuser_granted_at: datetime | None = None
    deactivated_at: datetime | None = None
    verified_at: datetime | None = None
    terms_accepted_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class UserCreate(schemas.CreateUpdateDictModel):
    email: EmailStr
    password: str
    terms_accepted_at: datetime | None = None


class UserUpdate(schemas.CreateUpdateDictModel):
    password: str | None = None
    email: EmailStr | None = None
    superuser_granted_at: datetime | None = None
    deactivated_at: datetime | None = None
    verified_at: datetime | None = None
    terms_accepted_at: datetime | None = None

    def create_update_dict(self):
        # Keep regular users from mutating privileged/account-state fields.
        return self.model_dump(
            exclude_unset=True,
            exclude={"id", "superuser_granted_at", "deactivated_at", "verified_at"},
        )
