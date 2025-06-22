from django.urls import path
from .views import (
    SensorDataListAPIView,
    SensorDataDetailAPIView,
    WatchSensorDataAPIView,
    health_check
)

urlpatterns = [
    path('sensor/watch/', WatchSensorDataAPIView.as_view()),
    path('sensor/', SensorDataListAPIView.as_view()),
    path('sensor/<str:device_id>/', SensorDataDetailAPIView.as_view()),
    path("health/", health_check),
]