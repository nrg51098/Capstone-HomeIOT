from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from homeiotapi.models import TempThreshold, AppUser
from homeiotapi.serializers import TempThresholdsSerializer

class TempThresholdsViewSet(ViewSet):

    # def create(self, request):

    #     tempthreshold = TempThreshold()
    #     tempthreshold.label = request.data["label"]

    #     try:
    #         tempthreshold.save()
    #         serializer = TempThresholdsSerializer(tempthreshold, context={'request': request})
    #         return Response(serializer.data)

    #     except ValidationError as ex:
    #         return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        try:
            tempthreshold = TempThreshold.objects.get(pk=pk)
            creator = AppUser.objects.get(user=request.auth.user)
            if tempthreshold.subscription.appuser.id == creator.id:
                serializer = TempThresholdsSerializer(tempthreshold, context={'request': request})
                return Response(serializer.data)
            else:
                return Response({'message': "No permissions"}, status=status.HTTP_400_BAD_REQUEST) 
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):

        try:
            tempthreshold = TempThreshold.objects.get(pk=pk)
            creator = AppUser.objects.get(user=request.auth.user)
            if tempthreshold.subscription.appuser.id == creator.id:        
                tempthreshold.min_temp = request.data["min_temp"]
                tempthreshold.max_temp = request.data["max_temp"]

                tempthreshold.save()
                return Response({"msg":"fields updated successfully"}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': "No permissions"}, status=status.HTTP_400_BAD_REQUEST)        
        
        except Exception as ex:
            return HttpResponseServerError(ex)
    # def destroy(self, request, pk=None):

    #     try:
    #         tempthreshold = TempThreshold.objects.get(pk=pk)
    #         tempthreshold.delete()

    #         return Response({}, status=status.HTTP_204_NO_CONTENT)

    #     except TempThreshold.DoesNotExist as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    #     except Exception as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def list(self, request):
    #     tags = TempThreshold.objects.all()

    #     serializer = TempThresholdsSerializer(
    #         tags, many=True, context={'request': request})
    #     return Response(serializer.data)
