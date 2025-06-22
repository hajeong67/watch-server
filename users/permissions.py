from rest_framework.permissions import BasePermission

class MiddlewareAuthenticated(BasePermission):
    def has_permission(self, request, view):
        print(">> [DEBUG] MiddlewareAuthenticated called")
        return bool(request.user and request.user.is_authenticated)