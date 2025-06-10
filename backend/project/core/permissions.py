from django.views import View
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request


class PublicReadOnly(BasePermission):
    """
    The request is a read-only if the method is in SAFE_METHODS.
    """

    def has_permission(self, request: Request, view: View) -> bool:
        return request.method in SAFE_METHODS


class IsAdminUser(BasePermission):
    """
    Allows access only to admin users (staff status).
    """

    def has_permission(self, request: Request, view: View) -> bool:
        from project.accounts.models import User

        return bool(
            request.user
            and request.user.is_authenticated
            and isinstance(request.user, User)
            and request.user.is_staff
        )
