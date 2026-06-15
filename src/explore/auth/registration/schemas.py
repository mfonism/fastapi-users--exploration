from datetime import datetime

from fastapi_users import schemas
from pydantic import EmailStr, Field

from ...utils.email import normalize_email


class UserCreate(schemas.CreateUpdateDictModel):
    email: EmailStr
    full_name: str
    password: str = Field(json_schema_extra={"writeOnly": True})
    terms_accepted_at: datetime

    def create_update_dict(self):
        user_dict = super().create_update_dict()
        user_dict["email"] = normalize_email(user_dict["email"])
        return user_dict
