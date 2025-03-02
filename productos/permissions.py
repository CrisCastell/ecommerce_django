from rest_framework import permissions

class IsClienteOStaff(permissions.BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser or request.user.is_staff:
            return True

        return request.user.groups.filter(name="clientes").exists()