from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from homeiotapi.models import TempHumiDataset, AppUser, Device
from homeiotapi.serializers import TempHumiDatasetsSerializer

class TempHumiDatasetsViewSet(ViewSet):

    def create(self, request):
        creator = AppUser.objects.get(user=request.auth.user)

        temphumidataset = TempHumiDataset()
        temphumidataset.device_id = request.data["device_id"]
        temphumidataset.temp = request.data["temp"]
        temphumidataset.humi = request.data["humi"]

        if request.data["timestamp"] is not None:
            temphumidataset.timestamp = request.data["timestamp"] 
        
        currentdevice = Device.objects.get(pk=request.data["device_id"])

        try:
            if currentdevice.appuser.id == creator.id:
                temphumidataset.save()
                serializer = TempHumiDatasetsSerializer(temphumidataset, context={'request': request})
                return Response(serializer.data)

            else:
                return Response({'message': "No permissions"}, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as ex:
            return HttpResponseServerError(ex)


    # def retrieve(self, request, pk=None):
    #     try:
    #         temphumidataset = TempHumiDataset.objects.get(pk=pk)
    #         serializer = TempDatasetsSerializer(temphumidataset, context={'request': request})
    #         return Response(serializer.data)
    #     except Exception as ex:
    #         return HttpResponseServerError(ex)

    # def update(self, request, pk=None):

    #     temphumidataset = TempHumiDataset.objects.get(pk=pk)
    #     temphumidataset.temp = request.data["temp"]

    #     temphumidataset.save()
    #     return Response({}, status=status.HTTP_204_NO_CONTENT)

    # def destroy(self, request, pk=None):

    #     try:
    #         temphumidataset = TempHumiDataset.objects.get(pk=pk)
    #         temphumidataset.delete()

    #         return Response({}, status=status.HTTP_204_NO_CONTENT)

    #     except TempHumiDataset.DoesNotExist as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    #     except Exception as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        # tempdatasets = TempHumiDataset.objects.all()

        tempdatasets = {}
        creator = AppUser.objects.get(user=request.auth.user)
        device_id = self.request.query_params.get('device_id', None)
        if device_id is not None:
            tempdatasets = TempHumiDataset.objects.all()
            tempdatasets = tempdatasets.filter(device__id=device_id)
            device = Device.objects.get(pk=device_id)
            if device.appuser.id != creator.id:
                tempdatasets = tempdatasets.filter(device__is_public =True)
            
            tempdatasets = tempdatasets.filter(device__is_active =True)
            # tempdatasets = tempdatasets.filter(device__appuser__id = creator_id)
        # tempdatasets = tempdatasets.filter(device__is_public =True)

        # if the device is public and the device is active then if any user provides the device_id for this device it shows up
        # if the device is private and the device is active then only user can see the device datasets if he provides the device_id in the url
        # if the device is not active then no body sees the data


        # These filters all you to do http://localhost:8000/devices?device_id=1

        serializer = TempHumiDatasetsSerializer(
            tempdatasets, many=True, context={'request': request})
        return Response(serializer.data)
