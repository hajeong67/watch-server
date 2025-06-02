from django.urls import path
from .views import (
    SensorDataListAPIView,
    SensorDataDetailAPIView,
    WatchSensorDataAPIView,
)

urlpatterns = [
    path('api/sensor/', SensorDataListAPIView.as_view(), name="sensor-data-list"),       # GET
    # path('api/sensor/', AddSensorDataAPIView.as_view(), name="add-sensor-data"),         # POST
    path('api/sensor/<str:device_id>/', SensorDataDetailAPIView.as_view(), name="sensor-data-detail"),  # GET, PUT, PATCH, DELETE
    path('api/sensor/watch/', WatchSensorDataAPIView.as_view(), name="watch-sensor"),
]