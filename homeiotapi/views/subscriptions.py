from homeiotapi.models.appuser import AppUser
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.fields import NullBooleanField
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from homeiotapi.models import Subscription
from homeiotapi.serializers import SubscriptionsSerializer
from datetime import datetime
from django.db.models import Q


class SubscriptionsViewSet(ViewSet):

    def retrieve(self, request, pk=None):

        try:
            subscription = Subscription.objects.get(pk=pk)
            serializer = SubscriptionsSerializer(
                subscription, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def list(self, request):
        subscriptions = Subscription.objects.all()
        device = request.query_params.get('device', None)
        user = request.query_params.get('user', None)
        if device is not None:
            subscriptions = subscriptions.filter(device_id=device)
        if user is not None:
            subscriptions = subscriptions.filter(appuser_id=user)
        serializer = SubscriptionsSerializer(
          subscriptions, many=True, context={'request': request})
        return Response(serializer.data)

    
    def create(self, request):
        try:
            user = AppUser.objects.get(pk=request.user.id)
            device_id = request.data["device_id"]
            device_notification = request.data["device_notification"]    
            subscription = Subscription()
            subscription.device_id = device_id
            subscription.device_notification = device_notification
            subscription.appuser = user

            try:
                Subscription.objects.get(device_id=device_id, appuser_id=user.id)
            except Subscription.DoesNotExist as ex:
                try:
                    subscription.save()
                    serializer = SubscriptionsSerializer(subscription, context={'request': request})
                    return Response(serializer.data, status=status.HTTP_201_CREATED)

                except ValidationError as ex:
                    return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as ex:
          return HttpResponseServerError(ex)
        
        return Response({}, status=status.HTTP_204_NO_CONTENT)
        
          


    def destroy(self, request, pk=None):

        try:
            if request.user.is_staff:
                subscription = Subscription.objects.get(pk=pk)
            else:
                subscription = Subscription.objects.get(pk=pk, appuser_id=request.user.id)
            
            subscription.delete()

            return Response({"msg":"subscription deleted"}, status=status.HTTP_204_NO_CONTENT)

        except subscription.DoesNotExist as ex:
          return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
          return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def update(self, request, pk=None):
        try:
            if request.user.is_staff:
                subscription = Subscription.objects.get(pk=pk)
            else:
                subscription = Subscription.objects.get(pk=pk, appuser_id=request.user.id)
            
            subscription.device_notification = request.data["device_notification"]
            subscription.save()

            return Response({"msg": "device_notification updated succesfully"}, status=status.HTTP_204_NO_CONTENT)

        except subscription.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)