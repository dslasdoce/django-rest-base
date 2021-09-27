# -*- coding: utf-8 -*-
from rest_framework.permissions import BasePermission, SAFE_METHODS


ADMIN_ONLY = []
PUBLIC_ENDPOINTS = {
    '/rest/v1/profiles': ['POST']
}


class BaseViewPermission(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """
    def has_permission(self, request, view):
        try:
            if request.user.is_authenticated:
                if request.path in ADMIN_ONLY:
                    if request.user.is_superuser or request.user.is_staff:
                        return True
                else:
                    return True

        except AttributeError:
            return False
        return False

    def has_object_permission(self, request, view, obj):
        try:
            if request.method in SAFE_METHODS:
                return True
            if (obj.user.id == request.user.id or request.user.is_staff
                    or request.user.is_superuser):
                return True
        except AttributeError:
            if (obj.id == request.user.id or request.user.is_staff
                    or request.user.is_superuser):
                return True

            if (obj.id == request.user or request.user.is_staff
                    or request.user.is_superuser):
                return True
        return False


class PublicReadPermission(BaseViewPermission):
    """
    This permission grants read access to anyone but write will require
    user authentication
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return super().has_permission(request, view)


class PublicCreatePermission(BaseViewPermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        else:
            return super().has_permission(request, view)
