from rest_framework import serializers
from homeiotapi.models import TempHumiDataset

class TempHumiDatasetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempHumiDataset
        fields = ('id', 'device','timestamp', 'temp', 'humi')
        depth = 2
