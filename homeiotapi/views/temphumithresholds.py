from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from homeiotapi.models import TempHumiThreshold, AppUser
from homeiotapi.serializers import TempHumiThresholdsSerializer

class TempHumiThresholdsViewSet(ViewSet):

    # def create(self, request):

    #     temphumithreshold = TempHumiThreshold()
    #     temphumithreshold.label = request.data["label"]

    #     try:
    #         temphumithreshold.save()
    #         serializer = TempHumiThresholdsSerializer(temphumithreshold, context={'request': request})
    #         return Response(serializer.data)

    #     except ValidationError as ex:
    #         return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        try:
            temphumithreshold = TempHumiThreshold.objects.get(pk=pk)
            creator = AppUser.objects.get(user=request.auth.user)
            if temphumithreshold.subscription.appuser.id == creator.id:
                serializer = TempHumiThresholdsSerializer(temphumithreshold, context={'request': request})
                return Response(serializer.data)
            else:
                return Response({'message': "No permissions"}, status=status.HTTP_401_UNAUTHORIZED) 
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):

        try:
            temphumithreshold = TempHumiThreshold.objects.get(pk=pk)
            creator = AppUser.objects.get(user=request.auth.user)
            if temphumithreshold.subscription.appuser.id == creator.id:        
                temphumithreshold.min_temp = request.data["min_temp"]
                temphumithreshold.max_temp = request.data["max_temp"]
                temphumithreshold.min_humi = request.data["min_humi"]
                temphumithreshold.max_humi = request.data["max_humi"]

                temphumithreshold.save()
                return Response({"msg":"fields updated successfully"}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': "No permissions"}, status=status.HTTP_401_UNAUTHORIZED)        
        
        except Exception as ex:
            return HttpResponseServerError(ex)
    # def destroy(self, request, pk=None):

    #     try:
    #         temphumithreshold = TempHumiThreshold.objects.get(pk=pk)
    #         temphumithreshold.delete()

    #         return Response({}, status=status.HTTP_204_NO_CONTENT)

    #     except TempHumiThreshold.DoesNotExist as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    #     except Exception as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def list(self, request):
    #     tags = TempHumiThreshold.objects.all()

    #     serializer = TempHumiThresholdsSerializer(
    #         tags, many=True, context={'request': request})
    #     return Response(serializer.data)
