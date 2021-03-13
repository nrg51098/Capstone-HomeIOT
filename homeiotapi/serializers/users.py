from rest_framework import serializers
from homeiotapi.models import AppUser
from django.contrib.auth import get_user_model


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        user = get_user_model()
        devices = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
        fields = ('id', 'user', 'address', 'profile_img_url',
                  'created_on', 'devices')
        depth = 3
