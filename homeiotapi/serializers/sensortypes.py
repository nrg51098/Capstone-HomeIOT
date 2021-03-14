from rest_framework import serializers
from homeiotapi.models import SensorType

class SensorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorType
        fields = ('id', 'label')
