from rest_framework import serializers
from homeiotapi.models import TempHumiThreshold

class TempHumiThresholdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempHumiThreshold
        fields = ('id', 'subscription', 'min_temp', 'max_temp', 'min_humi', 'max_humi')
        depth = 2
