from explore.app import app


def test_openapi_marks_password_fields_write_only() -> None:
    schemas = app.openapi()["components"]["schemas"]

    assert schemas["UserCreate"]["properties"]["password"]["writeOnly"] is True
    assert (
        schemas["PasswordChange"]["properties"]["current_password"]["writeOnly"] is True
    )
    assert schemas["PasswordChange"]["properties"]["new_password"]["writeOnly"] is True


def test_openapi_documents_logout_as_no_content() -> None:
    responses = app.openapi()["paths"]["/auth/logout"]["post"]["responses"]

    assert "204" in responses
    assert "200" not in responses
    assert "content" not in responses["204"]
