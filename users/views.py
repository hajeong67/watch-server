from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Watch
from watch.opensearch_client import client
from watch.opensearch_service import INDEX_NAME
from watch.serializers import SensorDataSerializer

User = get_user_model()

class RegisterWatchAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user  # 현재 로그인한 유저
        device_id = request.data.get("device_id")

        if not device_id:
            return Response({"error": "device_id는 필수입니다."}, status=status.HTTP_400_BAD_REQUEST)

        # OpenSearch에 해당 device_id가 있는지 확인
        query = {"query": {"match": {"device_id": device_id}}}
        search_response = client.search(index=INDEX_NAME, body=query)

        if not search_response["hits"]["hits"]:
            return Response({"error": "OpenSearch에 존재하지 않는 device_id입니다."}, status=status.HTTP_404_NOT_FOUND)

        # Django ORM에도 동일한 device_id가 존재하는지 확인
        if Watch.objects.filter(device_id=device_id).exists():
            return Response({"error": "이미 등록된 device_id입니다."}, status=status.HTTP_400_BAD_REQUEST)

        # Django ORM에 `device_id`와 유저 정보 저장
        watch = Watch.objects.create(device_id=device_id, user=user)

        return Response({"message": "워치 등록 완료!", "watch_id": watch.id}, status=status.HTTP_201_CREATED)

class WatchSensorDataAPIView(APIView):
    def post(self, request, *args, **kwargs):
        device_id = request.data.get("device_id")

        if not device_id:
            return Response({"error": "device_id는 필수입니다."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            watch = Watch.objects.get(device_id=device_id)
        except Watch.DoesNotExist:
            return Response({"error": "등록되지 않은 device_id입니다."}, status=status.HTTP_404_NOT_FOUND)

        serializer = SensorDataSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        response = client.index(index=INDEX_NAME, body=data)

        return Response({
            "message": "워치 데이터 저장 완료!",
            "users": watch.user.username,  # 유저 정보 반환
            "result": response
        }, status=status.HTTP_201_CREATED)
