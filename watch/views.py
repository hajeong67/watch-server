from watch.opensearch_client import client
from watch.opensearch_service import INDEX_NAME
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiTypes
from rest_framework import status
from watch.serializers import SensorDataSerializer
from emotion.modules.tasks import run_ppg_positioning

class SensorDataListAPIView(APIView):
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

# class AddSensorDataAPIView(APIView):
#     # permission_classes = [IsAuthenticated]
#
#     @extend_schema(
#         summary="Add sensor data",
#         description="Store new sensor data in OpenSearch.",
#         request=SensorDataSerializer,
#         responses={201: OpenApiTypes.OBJECT},
#     )
#     def post(self, request, *args, **kwargs):
#         serializer = SensorDataSerializer(data=request.data)
#
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             data = serializer.validated_data
#             response = client.index(index=INDEX_NAME, body=data)
#
#             return Response({"message": "데이터 저장 완료!", "result": response}, status=status.HTTP_201_CREATED)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SensorDataDetailAPIView(APIView):
    @extend_schema(
        summary="Get sensor data by device_id",
        description="Retrieve sensor data filtered by device_id.",
        responses={200: OpenApiTypes.OBJECT},
    )
    def get(self, request, device_id, *args, **kwargs):
        query = {"query": {"match": {"device_id": device_id}}}
        response = client.search(index=INDEX_NAME, body=query)

        serialized_data = SensorDataSerializer(
            [hit["_source"] for hit in response["hits"]["hits"]], many=True
        ).data

        return Response({"data": serialized_data})

    @extend_schema(
        summary="Update sensor data",
        description="Update existing sensor data in OpenSearch.",
        request=SensorDataSerializer,
        responses={200: OpenApiTypes.OBJECT},
    )
    def put(self, request, device_id, *args, **kwargs):
        serializer = SensorDataSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            query = {"query": {"match": {"device_id": device_id}}}
            search_response = client.search(index=INDEX_NAME, body=query)

            if not search_response["hits"]["hits"]:
                return Response({"error": "해당 device_id에 대한 데이터가 없습니다."}, status=status.HTTP_404_NOT_FOUND)

            doc_id = search_response["hits"]["hits"][0]["_id"]
            update_response = client.index(index=INDEX_NAME, id=doc_id, body=serializer.validated_data)

            return Response({"message": "데이터 업데이트 완료!", "result": update_response}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        summary="Partially update sensor data",
        description="Partially update existing sensor data in OpenSearch.",
        request=SensorDataSerializer,
        responses={200: OpenApiTypes.OBJECT},
    )
    def patch(self, request, device_id, *args, **kwargs):
        try:
            query = {"query": {"match": {"device_id": device_id}}}
            search_response = client.search(index=INDEX_NAME, body=query)

            if not search_response["hits"]["hits"]:
                return Response({"error": "해당 device_id에 대한 데이터가 없습니다."}, status=status.HTTP_404_NOT_FOUND)

            doc_id = search_response["hits"]["hits"][0]["_id"]
            update_body = {"doc": request.data}
            update_response = client.update(index=INDEX_NAME, id=doc_id, body=update_body)

            return Response({"message": "데이터 부분 업데이트 완료!", "result": update_response}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        summary="Delete sensor data",
        description="Delete sensor data from OpenSearch.",
        responses={200: OpenApiTypes.OBJECT},
    )
    def delete(self, request, device_id, *args, **kwargs):
        try:
            query = {"query": {"match": {"device_id": device_id}}}
            search_response = client.search(index=INDEX_NAME, body=query)

            if not search_response["hits"]["hits"]:
                return Response({"error": "해당 device_id에 대한 데이터가 없습니다."}, status=status.HTTP_404_NOT_FOUND)

            doc_id = search_response["hits"]["hits"][0]["_id"]
            delete_response = client.delete(index=INDEX_NAME, id=doc_id)

            return Response({"message": "데이터 삭제 완료!", "result": delete_response}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class WatchSensorDataAPIView(APIView):
    @extend_schema(
        summary="워치 센서 데이터 수신 및 실시간 추론",
        description="워치에서 수신된 PPG/ACC 데이터를 저장하고, 바로 실시간 추론을 수행합니다.",
        request=SensorDataSerializer,
        responses={201: SensorDataSerializer}
    )
    def post(self, request, *args, **kwargs):
        print("요청 유저:", request.user)
        if not request.user:
            return Response({"error": "인증되지 않은 디바이스입니다."}, status=status.HTTP_401_UNAUTHORIZED)
        print("✅ 인증 완료!")

        serializer = SensorDataSerializer(data=request.data)
        print("✅ 수신 데이터:", request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            data = serializer.validated_data
            data["user_id"] = request.user.id

            # OpenSearch 저장
            response = client.index(index=INDEX_NAME, body=data)
            print("📦 저장 완료:", response)

            # 동기 추론 수행
            result = run_ppg_positioning(data)
            print("🧠 추론 결과:", result)

            return Response({
                "message": "워치 데이터 저장 및 추론 완료",
                "opensearch_result": response,
                "inference_result": result
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)