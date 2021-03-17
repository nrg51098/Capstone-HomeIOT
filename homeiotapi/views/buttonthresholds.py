from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from homeiotapi.models import ButtonThreshold, AppUser
from homeiotapi.serializers import ButtonThresholdsSerializer

class ButtonThresholdsViewSet(ViewSet):

    # def create(self, request):

    #     buttonthreshold = ButtonThreshold()
    #     buttonthreshold.label = request.data["label"]

    #     try:
    #         buttonthreshold.save()
    #         serializer = ButtonThresholdsSerializer(buttonthreshold, context={'request': request})
    #         return Response(serializer.data)

    #     except ValidationError as ex:
    #         return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        try:
            buttonthreshold = ButtonThreshold.objects.get(pk=pk)
            creator = AppUser.objects.get(user=request.auth.user)
            if buttonthreshold.subscription.appuser.id == creator.id:
                serializer = ButtonThresholdsSerializer(buttonthreshold, context={'request': request})
                return Response(serializer.data)
            else:
                return Response({'message': "No permissions"}, status=status.HTTP_401_UNAUTHORIZED) 
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):

        try:
            buttonthreshold = ButtonThreshold.objects.get(pk=pk)
            creator = AppUser.objects.get(user=request.auth.user)
            if buttonthreshold.subscription.appuser.id == creator.id:        
                buttonthreshold.notify_if = request.data["notify_if"]                

                buttonthreshold.save()
                return Response({"msg":"fields updated successfully"}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': "No permissions"}, status=status.HTTP_401_UNAUTHORIZED)        
        
        except Exception as ex:
            return HttpResponseServerError(ex)
    # def destroy(self, request, pk=None):

    #     try:
    #         buttonthreshold = ButtonThreshold.objects.get(pk=pk)
    #         buttonthreshold.delete()

    #         return Response({}, status=status.HTTP_204_NO_CONTENT)

    #     except ButtonThreshold.DoesNotExist as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    #     except Exception as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def list(self, request):
    #     tags = ButtonThreshold.objects.all()

    #     serializer = ButtonThresholdsSerializer(
    #         tags, many=True, context={'request': request})
    #     return Response(serializer.data)
