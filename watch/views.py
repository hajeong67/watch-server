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
        summary="Receive and store sensor data from watch",
        description="Receive sensor data from watch and store it in OpenSearch.",
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

            return Response({"message": "워치 데이터 저장 완료!", "result": response}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)