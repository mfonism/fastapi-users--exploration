import uuid
from typing import Any

import jwt
from email_validator import EmailNotValidError
from fastapi import Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import BaseUserManager, UUIDIDMixin, exceptions
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.jwt import decode_jwt
from sqlalchemy.ext.asyncio import AsyncSession

from ...db.config import get_async_session
from ...settings import settings
from ...utils import clock
from ...utils.email import normalize_email
from ..exceptions import UserDeleted
from ..notifications import send_password_reset_request, send_verification_request
from .models import User


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.reset_password_token_secret
    verification_token_secret = settings.verification_token_secret

    def _raise_if_deleted(self, user: User) -> None:
        if user.is_deleted:
            raise UserDeleted()

    async def get_by_email(self, user_email: str) -> User:
        try:
            user_email = normalize_email(user_email)
        except EmailNotValidError:
            raise exceptions.UserNotExists() from None

        return await super().get_by_email(user_email)

    async def authenticate(self, credentials: OAuth2PasswordRequestForm):
        try:
            credentials.username = normalize_email(credentials.username)
        except EmailNotValidError:
            self.password_helper.hash(credentials.password)
            return None

        user = await super().authenticate(credentials)

        if user is not None:
            self._raise_if_deleted(user)

        return user

    async def request_verify(self, user: User, request: Request | None = None) -> None:
        self._raise_if_deleted(user)
        await super().request_verify(user, request)

    async def forgot_password(self, user: User, request: Request | None = None) -> None:
        self._raise_if_deleted(user)
        await super().forgot_password(user, request)

    async def verify(self, token: str, request: Request | None = None) -> User:
        try:
            return await super().verify(token, request)
        except exceptions.UserAlreadyVerified:
            return await self._get_already_verified_user(token)

    async def _get_already_verified_user(self, token: str) -> User:
        try:
            data = decode_jwt(
                token,
                self.verification_token_secret,
                [self.verification_token_audience],
            )
        except jwt.PyJWTError:
            raise exceptions.InvalidVerifyToken() from None

        try:
            email = data["email"]
        except KeyError:
            raise exceptions.InvalidVerifyToken() from None

        try:
            user = await self.get_by_email(email)
        except exceptions.UserNotExists:
            raise exceptions.InvalidVerifyToken() from None

        self._raise_if_deleted(user)
        return user

    async def _update(self, user: User, update_dict: dict[str, Any]) -> User:
        self._raise_if_deleted(user)
        return await super()._update(user, update_dict)

    async def on_after_register(self, user: User, request: Request | None = None):
        await self.request_verify(user, request)

    async def on_after_request_verify(
        self, user: User, token: str, request: Request | None = None
    ):
        await send_verification_request(
            recipient_email=user.email,
            recipient_name=user.full_name,
            token=token,
        )

    async def on_after_forgot_password(
        self, user: User, token: str, request: Request | None = None
    ):
        await send_password_reset_request(
            recipient_email=user.email,
            recipient_name=user.full_name,
            token=token,
        )

    async def on_after_login(
        self,
        user: User,
        request: Request | None = None,
        response: Response | None = None,
    ) -> None:
        await self.user_db.update(user, {"last_login_at": clock.utcnow()})


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
