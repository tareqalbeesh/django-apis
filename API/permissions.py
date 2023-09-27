from rest_framework import permissions
from django.http import HttpRequest


class MenuItemViewPermission(permissions.BasePermission):

    def has_permission(self, request: HttpRequest, view):
        if (request.method != 'GET'):
            return request.user.is_superuser or request.user.groups.filter(name='Manager').exists()
        else:
            return True


class ManagerViewPermission(permissions.BasePermission):
    def has_permission(self, request: HttpRequest, view):
        return request.user.is_superuser or request.user.groups.filter(name='Manager').exists()


class DeliveryCrewViewPermission(permissions.BasePermission):
    def has_permission(self, request: HttpRequest, view):
        return request.user.is_superuser or request.user.groups.filter(name='Manager').exists()


class SingleOrderViewPermission(permissions.BasePermission):
    def has_object_permission(self, request: HttpRequest, view, obj):
        if (request.method in ['GET', 'POST', 'PUT']):
            print('checking if the user is the same one')
            print(request.user == obj.user)
            if (request.user == obj.user or request.user.groups.filter(name='Manager').exists()):
                return True
            else:
                return False
        else:
            return request.user.groups.filter(name='Manager').exists()


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Manager').exists()


class IsDriver(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Delivery crew').exists()


class IsOnlyUser(permissions.BasePermission):
    def has_permission(self, request: HttpRequest, view):
        return not request.user.groups.filter(name='Delivery crew').exists() and not request.user.groups.filter(name='Manager').exists() and not request.user.is_superuser
