from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from watch.serializers import SensorDataSerializer
# from emotion.modules.tasks import run_ppg_positioning_task
from emotion.modules.tasks import run_ppg_positioning
from drf_spectacular.utils import extend_schema

# class SensorDataView(APIView):
#     """
#     워치에서 센서 데이터를 수신하고 PPG 기반 추론을 비동기로 실행하는 API View
#     """
#     def post(self, request, *args, **kwargs):
#         serializer = SensorDataSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         # Celery task로 비동기 처리 시작
#         run_ppg_positioning_task.delay(serializer.validated_data)
#         return Response({"message": "데이터 수신 및 처리 시작"}, status=status.HTTP_202_ACCEPTED)
#
class SensorDataView(APIView):
    @extend_schema(
        summary="센서 데이터 업로드 및 추론 실행",
        description="워치에서 수집한 PPG/ACC 데이터를 업로드하고 실시간 추론 결과를 반환합니다.",
        request=SensorDataSerializer,
        responses={200: SensorDataSerializer}
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        if not user:
            return Response({"error": "인증되지 않은 워치입니다."}, status=401)
        serializer = SensorDataSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 동기 처리
        result = run_ppg_positioning(serializer.validated_data)

        return Response({"message": "데이터 처리 완료", "result": result}, status=status.HTTP_200_OK)


