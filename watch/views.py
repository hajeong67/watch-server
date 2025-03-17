from watch.opensearch_client import client
from watch.opensearch_service import INDEX_NAME
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiTypes
from rest_framework import status
from watch.serializers import SensorDataSerializer

class SensorDataListAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get all sensor data",
        description="Retrieve all sensor data stored in OpenSearch.",
        responses={200: OpenApiTypes.OBJECT},
    )
    def get(self, request, *args, **kwargs):
        query = {"query": {"match_all": {}}}  # 모든 데이터 조회
        response = client.search(index=INDEX_NAME, body=query)

        serialized_data = SensorDataSerializer(
            [hit["_source"] for hit in response["hits"]["hits"]], many=True
        ).data

        return Response({"data": serialized_data})

class SensorDataByDeviceAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get sensor data by device_id",
        description="Retrieve sensor data filtered by device_id.",
        responses={200: OpenApiTypes.OBJECT},
    )
    def get(self, request, device_id, *args, **kwargs):
        query = {"query": {"match": {"device_id": device_id}}}  # 특정 device_id 검색
        response = client.search(index=INDEX_NAME, body=query)

        serialized_data = SensorDataSerializer(
            [hit["_source"] for hit in response["hits"]["hits"]], many=True
        ).data

        return Response({"data": serialized_data})

class AddSensorDataAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Add sensor data",
        description="Store new sensor data in OpenSearch.",
        request=SensorDataSerializer,
        responses={201: OpenApiTypes.OBJECT},
    )
    def post(self, request, *args, **kwargs):
        serializer = SensorDataSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            data = serializer.validated_data
            response = client.index(index=INDEX_NAME, body=data)

            return Response({"message": "데이터 저장 완료!", "result": response}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
