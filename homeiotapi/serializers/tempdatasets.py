from rest_framework import serializers
from homeiotapi.models import TempDataset

class TempDatasetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempDataset
        fields = ('id', 'device','timestamp', 'temp')
        depth = 2
