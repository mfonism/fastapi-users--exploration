INTERNAL_USER_FIELDS = {
    "deactivated_at",
    "deleted_at",
    "last_login_at",
    "superuser_granted_at",
    "terms_accepted_at",
    "updated_at",
    "email_verified_at",
}


def assert_internal_user_fields_hidden(payload: dict[str, object]) -> None:
    exposed_fields = INTERNAL_USER_FIELDS & payload.keys()
    assert not exposed_fields, f"Internal user fields exposed: {sorted(exposed_fields)}"
