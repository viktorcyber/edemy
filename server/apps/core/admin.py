from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session


class AdminRequiredMixin:
    """Mixin to require admin role."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin:
            from django.core.exceptions import PermissionDenied

            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


admin.site.register([LogEntry, Permission, ContentType, Session])
