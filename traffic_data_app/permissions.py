from rest_framework import permissions

class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Permite acesso total apenas a utilizadores administradores.
    Permite apenas acesso de leitura (GET, HEAD, OPTIONS) a outros utilizadores.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.is_superuser