from rest_framework import serializers
from homeiotapi.models import UserPreference

class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        appuser = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
        fields = ('unit', 'appuser', 'fail_notification', 'threshold_notification')
        depth = 2
        