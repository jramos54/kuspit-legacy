from rest_framework import permissions
from django.http import HttpResponseForbidden


class IsSuperUserOrClient(permissions.BasePermission):
    """
    Permiso personalizado para permitir solo a usuarios con los grupos 'dypfe_superuser' o 'dypfe_client' acceder.
    """
    def has_permission(self, request, view):
        # allowed_groups = ['dypfe_superuser', 'dypfe_client']
        # user_groups = request.user.groups.values_list('name', flat=True)
        # return any(group in allowed_groups for group in user_groups)
        if request.user and request.user.groups.filter(name__in=['dypfe_superuser','dypfe_client']):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)

class IsAdmin(permissions.BasePermission):
    """
    Permiso personalizado para permitir solo a usuarios en el grupo 'dypfe_admin' acceder.
    """
    def has_permission(self, request, view):
        # allowed_groups = ['dypfe_admin']
        # user_groups = request.user.groups.values_list('name', flat=True)
        # return any(group in allowed_groups for group in user_groups)

        if request.user and request.user.groups.filter(name='dypfe_admin'):
            return True
        return False

class IsAnalista(permissions.BasePermission):
    """
    Permiso personalizado para permitir solo a usuarios en el grupo 'dypfe_analista' acceder.
    """
    def has_permission(self, request, view):
        # allowed_groups = ['dypfe_analista']
        # user_groups = request.user.groups.values_list('name', flat=True)
        # return any(group in allowed_groups for group in user_groups)
        if request.user and request.user.groups.filter(name='dypfe_analista'):
            return True
        return False

class IsAutorizador(permissions.BasePermission):
    """
    Permiso personalizado para permitir solo a usuarios en el grupo 'dypfe_autorizador' acceder.
    """
    def has_permission(self, request, view):
        # allowed_groups = ['dypfe_autorizador']
        # user_groups = request.user.groups.values_list('name', flat=True)
        # return any(group in allowed_groups for group in user_groups)
        if request.user and request.user.groups.filter(name='dypfe_autorizador'):
            return True
        return False


class IsUser(permissions.BasePermission):
    """
    Permiso personalizado para permitir solo a usuarios en el grupo 'dypfe_user' acceder.
    """
    def has_permission(self, request, view):
        # allowed_groups = ['dypfe_user']
        # user_groups = request.user.groups.values_list('name', flat=True)
        # return any(group in allowed_groups for group in user_groups
        if request.user and request.user.groups.filter(name='dypfe_user'):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
