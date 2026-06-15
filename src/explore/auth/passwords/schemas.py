from pydantic import BaseModel, Field


class PasswordChange(BaseModel):
    current_password: str = Field(json_schema_extra={"writeOnly": True})
    new_password: str = Field(json_schema_extra={"writeOnly": True})
