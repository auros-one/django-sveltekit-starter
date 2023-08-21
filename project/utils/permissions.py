from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request

from django.views import View


class PublicReadOnly(BasePermission):
    """
    The request is a read-only if the method is in SAFE_METHODS.
    """

    def has_permission(self, request: Request, view: View) -> bool:
        return request.method in SAFE_METHODS
