import uuid
from datetime import datetime

from fastapi_users import schemas
from pydantic import ConfigDict, EmailStr


class UserRead(schemas.CreateUpdateDictModel):
    id: uuid.UUID
    email: EmailStr
    created_at: datetime
    updated_at: datetime
    last_login_at: datetime | None = None
    superuser_granted_at: datetime | None = None
    deactivated_at: datetime | None = None
    deleted_at: datetime | None = None
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
    deleted_at: datetime | None = None
    verified_at: datetime | None = None
    terms_accepted_at: datetime | None = None

    def create_update_dict(self):
        # Keep regular users from mutating privileged/account-state fields.
        return self.model_dump(
            exclude_unset=True,
            exclude={
                "id",
                "created_at",
                "updated_at",
                "last_login_at",
                "superuser_granted_at",
                "deactivated_at",
                "deleted_at",
                "verified_at",
            },
        )
