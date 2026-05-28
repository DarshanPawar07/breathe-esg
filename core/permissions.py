# permissions.py
from rest_framework.permissions import BasePermission


class IsAnalystUser(BasePermission):
    """
    Placeholder analyst permission.
    In production this would use RBAC.
    """

    def has_permission(self, request, view):
        return True