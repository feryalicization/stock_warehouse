from rest_framework.permissions import BasePermission

class IsAdminUserOrStaff(BasePermission):
    """
    Allows access only to admin (superuser) or staff users.
    """
    def has_permission(self, request, view):
        return request.user and (request.user.is_superuser or request.user.is_staff)
