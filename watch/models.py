# from django.db import models
# from django.contrib.postgres.fields import JSONField
#
# class SensorData(models.Model):
#     time = models.BigIntegerField()  # Unix time (ms)
#     device_id = models.CharField(max_length=255)
#     acc = JSONField()  # Stores x, y, z acceleration data as JSON
#     ppg = JSONField()  # Stores PPG sensor data as JSON array
#
#     def __str__(self):
#         return f"SensorData {self.device_id} at {self.time}"
