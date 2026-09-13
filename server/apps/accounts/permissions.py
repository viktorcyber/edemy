from rest_framework import permissions


def has_clerk_permission(permission: str):
    class _HasClerkPermission(permissions.BasePermission):
        def has_permission(self, request, view):
            state = request.auth
            if state is None:
                return False
            org_permissions = state.payload.get("org_permissions") or []
            return permission in org_permissions

    return _HasClerkPermission


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user