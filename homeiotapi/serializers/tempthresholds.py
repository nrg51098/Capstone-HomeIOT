from rest_framework import serializers
from homeiotapi.models import TempThreshold

class TempThresholdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempThreshold
        fields = ('id', 'subscription', 'min_temp', 'max_temp')
        depth = 2
