from django.urls import path
from emotion.modules.views import SensorDataView

urlpatterns = [
    path("ppg/", SensorDataView.as_view(), name="inference-data"),
]
