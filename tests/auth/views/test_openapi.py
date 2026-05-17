from explore.app import app


def test_openapi_marks_password_fields_write_only() -> None:
    schemas = app.openapi()["components"]["schemas"]

    assert schemas["UserCreate"]["properties"]["password"]["writeOnly"] is True
    assert (
        schemas["PasswordChange"]["properties"]["current_password"]["writeOnly"] is True
    )
    assert schemas["PasswordChange"]["properties"]["new_password"]["writeOnly"] is True
