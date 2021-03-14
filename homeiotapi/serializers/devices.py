from rest_framework import serializers
from homeiotapi.models import Device


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        appuser = serializers.PrimaryKeyRelatedField(
            many=False, read_only=True)
        location = serializers.PrimaryKeyRelatedField(
            many=False, read_only=True)
        sensor_type = serializers.PrimaryKeyRelatedField(
            many=False, read_only=True)
        fields = ('id', 'appuser', 'name', 'location',
                  'created_datetime', 'device_img_url', 'hardware_number', 'sensor_type', 'tag',
                  'is_active', 'is_public')
        depth = 2
