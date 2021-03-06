from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from homeiotapi.models import AppUser
from homeiotapi.serializers import UsersSerializer
from django.contrib.auth.models import User


class UsersViewSet(ViewSet):

    def retrieve(self, request, pk=None):
        try:
            user = AppUser.objects.get(pk=pk)
            serializer = UsersSerializer(user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        users = AppUser.objects.all()
        serializer = UsersSerializer(
            users, many=True, context={'request': request})
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        appUser = AppUser.objects.get(pk=pk)
        serializer = UsersSerializer(appUser, data=request.data, partial=True)
        newUserObj = request.data.pop('user')
        baseUser = User.objects.get(pk=newUserObj["id"])
        for key, val in newUserObj.items():
            print(key, val)
            if (key == "id"):
                continue
            setattr(baseUser, key, val)
            # baseUser.key = val        
        baseUser.save()
        for key, val in request.data.items():
            setattr(serializer, key, val)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
