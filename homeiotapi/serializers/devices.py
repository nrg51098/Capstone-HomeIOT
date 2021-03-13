from rest_framework import serializers
from homeiotapi.models import Device


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        rareuser = serializers.PrimaryKeyRelatedField(
            many=False, read_only=True)
        category = serializers.PrimaryKeyRelatedField(
            many=False, read_only=True)
        fields = ('id', 'appuser', 'name', 'location',
                  'created_datetime', 'device_img_url', 'hardware_number', 'sensor_type', 'tag',
                  'is_active', 'is_public')
        depth = 2
