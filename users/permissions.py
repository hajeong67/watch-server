from rest_framework.permissions import BasePermission

class IsDeviceAuthenticated(BasePermission):
    def has_permission(self, request, view):
        print(">> [DEBUG] MiddlewareAuthenticated called")
        print(">> [DEBUG] is_authenticated:", request.user.is_authenticated)
        print(f">> [DEBUG] user instance: {type(request.user)}")
        return bool(request.user and request.user.is_authenticated)