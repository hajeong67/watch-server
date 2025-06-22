from rest_framework.permissions import BasePermission

class MiddlewareAuthenticated(BasePermission):
    """
    미들웨어로 인증된 사용자만 접근 가능
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
