from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from homeiotapi.models import TempDataset, AppUser, Device
from homeiotapi.serializers import TempDatasetsSerializer

class TempDatasetsViewSet(ViewSet):

    def create(self, request):
        creator = AppUser.objects.get(user=request.auth.user)

        tempdataset = TempDataset()
        tempdataset.device_id = request.data["device_id"]
        tempdataset.temp = request.data["temp"]

        if request.data["timestamp"] is not None:
            tempdataset.timestamp = request.data["timestamp"] 
        
        currentdevice = Device.objects.get(pk=request.data["device_id"])

        try:
            if currentdevice.appuser.id == creator.id:
                tempdataset.save()
                serializer = TempDatasetsSerializer(tempdataset, context={'request': request})
                return Response(serializer.data)

            else:
                return Response({'message': "No permissions"}, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as ex:
            return HttpResponseServerError(ex)


    # def retrieve(self, request, pk=None):
    #     try:
    #         tempdataset = TempDataset.objects.get(pk=pk)
    #         serializer = TempDatasetsSerializer(tempdataset, context={'request': request})
    #         return Response(serializer.data)
    #     except Exception as ex:
    #         return HttpResponseServerError(ex)

    # def update(self, request, pk=None):

    #     tempdataset = TempDataset.objects.get(pk=pk)
    #     tempdataset.temp = request.data["temp"]

    #     tempdataset.save()
    #     return Response({}, status=status.HTTP_204_NO_CONTENT)

    # def destroy(self, request, pk=None):

    #     try:
    #         tempdataset = TempDataset.objects.get(pk=pk)
    #         tempdataset.delete()

    #         return Response({}, status=status.HTTP_204_NO_CONTENT)

    #     except TempDataset.DoesNotExist as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    #     except Exception as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        # tempdatasets = TempDataset.objects.all()

        tempdatasets = {}
        creator = AppUser.objects.get(user=request.auth.user)
        device_id = self.request.query_params.get('device_id', None)
        if device_id is not None:
            tempdatasets = TempDataset.objects.all()
            tempdatasets = tempdatasets.filter(device__id=device_id)
            device = Device.objects.get(pk=device_id)
            if device.appuser.id != creator.id:
                tempdatasets = tempdatasets.filter(device__is_public =True)
            
            tempdatasets = tempdatasets.filter(device__is_active =True)
            # tempdatasets = tempdatasets.filter(device__appuser__id = creator_id)
        # tempdatasets = tempdatasets.filter(device__is_public =True)

        # These filters all you to do http://localhost:8000/devices?location=1 or
        # http://localhost:8000/devices?user=1 or
        # http://localhost:8000/devices?location=1&user=2

        serializer = TempDatasetsSerializer(
            tempdatasets, many=True, context={'request': request})
        return Response(serializer.data)
