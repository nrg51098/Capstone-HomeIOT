from homeiotapi.models.appuser import AppUser
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.fields import NullBooleanField
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from homeiotapi.models import Subscription, TempThreshold, TempHumiThreshold, ButtonThreshold, Device, buttonthreshold
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
                    device = Device.objects.get(pk=device_id)
                    if device is not None:
                        subscription.save()
                        print(device.sensor_type_id)
                        if device.sensor_type_id == 1:
                            tempthreshold = TempThreshold()
                            tempthreshold.subscription_id = subscription.id
                            tempthreshold.min_temp = 11.00
                            tempthreshold.max_temp = 89.00
                            tempthreshold.save()
                        elif device.sensor_type_id == 2:
                            temphumithreshold = TempHumiThreshold()
                            temphumithreshold.subscription_id = subscription.id
                            temphumithreshold.min_temp = 11.00
                            temphumithreshold.max_temp = 89.00
                            temphumithreshold.min_humi = 20.00
                            temphumithreshold.max_humi = 80.00
                            temphumithreshold.save()
                        elif device.sensor_type_id == 3:
                            buttonthreshold = ButtonThreshold()
                            buttonthreshold.subscription_id = subscription.id
                            buttonthreshold.notify_if = False
                            buttonthreshold.save()
                    else:
                        return Response({'reason': "something went wrong"}, status=status.HTTP_400_BAD_REQUEST)    

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