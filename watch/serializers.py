from rest_framework import serializers

class AccelerometerSerializer(serializers.Serializer):
    x = serializers.IntegerField()
    y = serializers.IntegerField()
    z = serializers.IntegerField()

class SensorDataSerializer(serializers.Serializer):
    time = serializers.IntegerField()
    device_id = serializers.CharField()
    acc = AccelerometerSerializer()
    ppg = serializers.ListField(child=serializers.IntegerField())
