from rest_framework import serializers

class SensorDataSerializer(serializers.Serializer):
    time = serializers.IntegerField()
    device_id = serializers.CharField(max_length=100)
    acc = serializers.ListField(child=serializers.ListField(child=serializers.IntegerField()))  # 중첩 리스트
    ppg = serializers.ListField(child=serializers.IntegerField())