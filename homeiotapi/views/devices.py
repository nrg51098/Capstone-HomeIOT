from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from homeiotapi.models import Device, AppUser, Tag, Location, SensorType
from homeiotapi.serializers import DeviceSerializer
from rest_framework.decorators import action


class DevicesViewSet(ViewSet):

    def create(self, request):
        creator = AppUser.objects.get(user=request.auth.user)

        device = Device()
        device.name = request.data["name"]
        device.device_img_url = request.data["image_url"]
        device.hardware_number = request.data["hardware_number"]        
        device.appuser = creator

        location = Location.objects.get(pk=request.data["location_id"])
        device.location = location

        sensor_type = SensorType.objects.get(pk=request.data["sensor_type_id"])
        device.sensor_type = sensor_type

        try:
            device.save()
            device.tag.set(request.data["tag"])
            device.save()
            serializer = DeviceSerializer(device, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            device = Device.objects.get(pk=pk)
            serializer = DeviceSerializer(device, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        device = Device.objects.get(pk=pk)
        device.name = request.data["name"]
        device.device_img_url = request.data["image_url"]
        device.hardware_number = request.data["hardware_number"]
        

        location = Location.objects.get(pk=request.data["location_id"])
        device.location = location

        sensor_type = SensorType.objects.get(pk=request.data["sensor_type_id"])
        device.sensor_type = sensor_type

        device.tag.set(request.data["tag"])
        device.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        try:
            # If user is an admin (is_staff == true), then we can just
            # delete the device by pk.  Otherwise, we should verify that
            # the user owns that device before deleting it.
            if request.user.is_staff:
                device = Device.objects.get(pk=pk)
            else:
                device = Device.objects.get(pk=pk, appuser_id=request.user.id)

            device.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except device.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        devices = Device.objects.all()
        location = self.request.query_params.get('location', None)
        sensor_type = self.request.query_params.get('sensor_type', None)
        user = self.request.query_params.get('user', None)

        # These filters all you to do http://localhost:8000/devices?location=1 or
        # http://localhost:8000/devices?user=1 or
        # http://localhost:8000/devices?location=1&user=2

        if location is not None:
            devices = devices.filter(location__id=location)

        if sensor_type is not None:
            devices = devices.filter(sensor_type__id=sensor_type)

        if user is not None:
            devices = devices.filter(appuser__id=user)

        serializer = DeviceSerializer(
            devices, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=['POST'], detail=True)
    def remove_tag(self, request, pk=None):

        try:
            device = Device.objects.get(pk=pk)
            tag = Tag.objects.get(pk=request.data['tag_id'])
            device.tag.remove(tag)

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Device.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Tag.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, pk=None):
        device= Device.objects.get(pk=pk)
        serializer = DeviceSerializer(device, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)