from functools import lru_cache

from clerk_backend_api import Clerk
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()


@lru_cache
def get_clerk() -> Clerk:
    return Clerk(bearer_auth=settings.CLERK_SECRET_KEY)


class ClerkWebhookService:
    @classmethod
    def handle_user_created_or_updated(cls, data: dict):
        email_addresses = data.get("email_addresses") or []
        primary_email_id = data.get("primary_email_address_id")
        email = next(
            (
                addr.get("email_address")
                for addr in email_addresses
                if addr.get("id") == primary_email_id
            ),
            email_addresses[0].get("email_address") if email_addresses else "",
        )

        avatar = data.get("image_url") or data.get("profile_image_url")
        is_banned = data.get("banned", False) or data.get("locked", False)

        defaults = {
            "email": email,
            "username": data.get("username") or "",
            "first_name": data.get("first_name") or "",
            "last_name": data.get("last_name") or "",
            "is_active": not is_banned,
            "picture": avatar,
        }

        with transaction.atomic():
            user, created = User.objects.get_or_create(id=data["id"], defaults=defaults)
            if not created:
                for key, value in defaults.items():
                    setattr(user, key, value)
                user.save(update_fields=list(defaults.keys()))
            return user

    @classmethod
    def handle_user_deleted(cls, clerk_id: str):
        with transaction.atomic():
            User.objects.filter(id=clerk_id).update(is_active=False)
