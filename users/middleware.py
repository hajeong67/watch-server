# import json
# from django.utils.deprecation import MiddlewareMixin
# from users.models import Watch
# from django.contrib.auth.models import AnonymousUser
# from django.contrib.auth import login
#
# class DeviceIDMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         if request.method != "POST":
#             return
#
#         content_type = request.META.get("CONTENT_TYPE", "")
#         if "application/json" not in content_type:
#             request.user = AnonymousUser()
#             request._cached_user = AnonymousUser()
#             print("Content-Type이 application/json이 아님")
#             return
#
#         try:
#             data = request.body.decode("utf-8")
#             parsed_data = json.loads(data)
#             device_id = parsed_data.get("device_id")
#             print(f"device_id 추출 성공: {device_id}")
#         except Exception as e:
#             device_id = None
#             print(f"JSON 파싱 실패: {e}")
#
#         if device_id:
#             try:
#                 watch = Watch.objects.select_related("user").get(device_id=device_id)
#                 request.user = watch.user
#                 request._cached_user = watch.user
#                 login(request, watch.user, backend='django.contrib.auth.backends.ModelBackend')
#                 print(f"인증 성공! user: {request.user.username} (user.id: {request.user.id})")
#             except Watch.DoesNotExist:
#                 request.user = AnonymousUser()
#                 request._cached_user = AnonymousUser()
#                 print(f"인증 실패! device_id {device_id} 찾을 수 없음")
#         else:
#             request.user = AnonymousUser()
#             request._cached_user = AnonymousUser()
#             print("device_id 없음")