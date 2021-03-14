from rest_framework import serializers
from homeiotapi.models import Subscription

class SubscriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        follower_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
        author_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
        fields = ('id', 'appuser', 'device', 'sub_unsub_date', 'device_notification')
        depth = 2
        