from django.urls import path
from watch.views import SensorDataListAPIView, SensorDataByDeviceAPIView, AddSensorDataAPIView, UpdateSensorDataAPIView, PartialUpdateSensorDataAPIView, DeleteSensorDataAPIView

urlpatterns = [
    path('api/sensor/list', SensorDataListAPIView.as_view(), name="sensor-data-list"),
    path('api/sensor/list-id/<str:device_id>/', SensorDataByDeviceAPIView.as_view(), name="sensor-data-by-device"),
    path('api/sensor/add/', AddSensorDataAPIView.as_view(), name="add-sensor-data"),
    path('api/sensor/update/<str:device_id>/', UpdateSensorDataAPIView.as_view(), name="update-sensor-data"),
    path('api/sensor/patch/<str:device_id>/', PartialUpdateSensorDataAPIView.as_view(), name="patch-sensor-data"),
    path('api/sensor/delete/<str:device_id>/', DeleteSensorDataAPIView.as_view(), name="delete-sensor-data"),
]