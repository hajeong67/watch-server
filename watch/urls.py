from django.urls import path
from watch.views import AddSensorDataAPIView, SensorDataListAPIView, SensorDataByDeviceAPIView

urlpatterns = [
    path('api/list-data/', SensorDataListAPIView.as_view(), name="sensor-data-list"),  # 모든 데이터 조회
    path('api/list-data-id/<str:device_id>/', SensorDataByDeviceAPIView.as_view(), name="sensor-data-by-device"),  # 특정 device_id 조회
    path('api/add-data/', AddSensorDataAPIView.as_view(), name="add-sensor-data"),  # 데이터 추가
]

