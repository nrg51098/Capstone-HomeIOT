from rest_framework import serializers
from homeiotapi.models import ButtonThreshold

class ButtonThresholdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ButtonThreshold
        fields = ('id', 'subscription', 'notify_if')
        depth = 2
