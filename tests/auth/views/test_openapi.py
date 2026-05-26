import pytest

from explore.app import app


def test_openapi_marks_password_fields_write_only() -> None:
    schemas = app.openapi()["components"]["schemas"]

    assert schemas["UserCreate"]["properties"]["password"]["writeOnly"] is True
    assert (
        schemas["PasswordChange"]["properties"]["current_password"]["writeOnly"] is True
    )
    assert schemas["PasswordChange"]["properties"]["new_password"]["writeOnly"] is True


@pytest.mark.parametrize(
    ("path", "method"),
    [
        ("/auth/logout", "post"),
        ("/auth/change-password", "post"),
        ("/auth/deactivate", "post"),
        ("/users/me", "delete"),
    ],
)
def test_openapi_documents_empty_commands_as_no_content(
    path: str,
    method: str,
) -> None:
    responses = app.openapi()["paths"][path][method]["responses"]

    assert "204" in responses, f"{method.upper()} {path} should document 204"
    assert "200" not in responses, f"{method.upper()} {path} should not document 200"
    assert "content" not in responses["204"], (
        f"{method.upper()} {path} 204 response should not document content"
    )
