from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """
    Permet uniquement aux administrateurs d'accéder aux vues protégées.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
