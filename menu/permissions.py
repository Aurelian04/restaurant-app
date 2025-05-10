from rest_framework import permissions


class IsStaffUser(permissions.BasePermission):
    """Manage staff accses for menu."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)