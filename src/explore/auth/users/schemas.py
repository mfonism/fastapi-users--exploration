import uuid
from datetime import datetime

from fastapi_users import schemas
from pydantic import ConfigDict, EmailStr


class CurrentUserRead(schemas.CreateUpdateDictModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CurrentUserUpdate(schemas.CreateUpdateDictModel):
    full_name: str | None = None

    model_config = ConfigDict(extra="forbid")

    def create_update_dict(self):
        return self.model_dump(exclude_unset=True)
