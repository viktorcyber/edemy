from dataclasses import dataclass

from clerk_backend_api import AuthenticateRequestOptions, authenticate_request
from clerk_backend_api.security.types import AuthErrorReason
from django.conf import settings
from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


@dataclass
class ClerkUser:
    id: str
    payload: dict

    is_authenticated: bool = True
    is_anonymous: bool = False
    is_active: bool = True

    def __str__(self) -> str:
        return self.id


class ClerkAuthentication(BaseAuthentication):
    """
    Production-grade DRF Authentication for Clerk.
    Verifies JWT token using Clerk's JWKS.
    """

    def authenticate(self, request):
        if "Authorization" not in request.headers:
            return None

        try:
            state = authenticate_request(
                request,
                AuthenticateRequestOptions(
                    secret_key=settings.CLERK_SECRET_KEY,
                    jwt_key=settings.CLERK_JWT_KEY,
                    authorized_parties=settings.CLERK_AUTHORIZED_PARTIES,
                    accepts_token=["session_token"],
                ),
            )
            if not state.is_signed_in:
                if state.reason is AuthErrorReason.SESSION_TOKEN_MISSING:
                    return None
                raise AuthenticationFailed(
                    detail=state.reason.name if state.reason else "unauthorized",
                    code=status.HTTP_401_UNAUTHORIZED,
                )

            user = ClerkUser(id=state.payload["sub"], payload=state.payload)
            return (user, state)
        except Exception as e:  # noqa: BLE001
            request.error_message = str(e)
            return None

    def authenticate_header(self, request):
        return "Bearer"
