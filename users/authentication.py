from rest_framework.authentication import BaseAuthentication
from django.contrib.auth.models import AnonymousUser
from users.models import Watch


class DeviceIDAuthentication(BaseAuthentication):
    """
    POST JSON body 또는 쿼리스트링의 device_id 로 사용자 인증
    """
    def authenticate(self, request):
        device_id = (
            request.data.get("device_id")
            if isinstance(request.data, dict) else None
        ) or request.query_params.get("device_id")

        if not device_id:
            return None                        # 다른 인증 방식에 양보

        try:
            watch = Watch.objects.select_related("user").get(device_id=device_id)
            return (watch.user, None)          # (user, auth) 튜플
        except Watch.DoesNotExist:
            return (AnonymousUser(), None)
