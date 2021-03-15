from rest_framework import serializers
from homeiotapi.models import ButtonDataset

class ButtonDatasetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ButtonDataset
        fields = ('id', 'device','timestamp', 'is_on')
        depth = 2
