from watch.opensearch_client import client
from watch.opensearch_setup import INDEX_NAME
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiTypes
from rest_framework import status
from watch.serializers import SensorDataSerializer
from emotion.modules.tasks import run_ppg_positioning
import time
from users.authentication import DeviceIDAuthentication
from users.permissions import IsDeviceAuthenticated

class SensorDataListAPIView(APIView):
    """Data-Stream 전체 또는 필터링 없이 최근 데이터 조회 (GET)"""
    @extend_schema(
        summary="센서 데이터 전체 조회",
        description="Data Stream(alias)에 저장된 모든 데이터를 반환합니다.",
        responses={200: OpenApiTypes.OBJECT},
    )
    def get(self, request, *args, **kwargs):
        query = {"query": {"match_all": {}}}
        res   = client.search(index=INDEX_NAME, body=query)
        data  = [hit["_source"] for hit in res["hits"]["hits"]]
        return Response({"data": data})

class SensorDataDetailAPIView(APIView):
    """특정 device_id 로 조회 전용 (GET)"""
    @extend_schema(
        summary="device_id별 조회",
        description="device_id 로 필터링된 센서 데이터를 반환합니다.",
        responses={200: OpenApiTypes.OBJECT},
    )
    def get(self, request, device_id, *args, **kwargs):
        query = {"query": {"match": {"device_id": device_id}}}
        res   = client.search(index=INDEX_NAME, body=query)
        data  = [hit["_source"] for hit in res["hits"]["hits"]]
        return Response({"data": data})

class WatchSensorDataAPIView(APIView):
    """워치에서 전송 → 저장 → 실시간 추론 (POST)"""

    authentication_classes = [DeviceIDAuthentication]
    permission_classes = [IsDeviceAuthenticated]

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"error": "인증 필요"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = SensorDataSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 데이터 가공
        data = serializer.validated_data
        data.setdefault("time", int(time.time() * 1000))  # epoch_millis
        data["@timestamp"] = data["time"]
        data["user"] = {
            "id":       request.user.id,
            "username": request.user.username,
            "email":    request.user.email,
        }

        infer_res = run_ppg_positioning(data)

        return Response({
            "message": "저장 및 추론 완료",
            "inference_result":  infer_res,
        }, status=status.HTTP_201_CREATED)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def health_check(request):
    return JsonResponse({"status": "ok"})
