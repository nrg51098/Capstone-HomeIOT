from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from homeiotapi.models import SensorType
from homeiotapi.serializers import SensorTypeSerializer

class SensorTypesViewSet(ViewSet):

    def create(self, request):

        sensortype = SensorType()
        sensortype.label = request.data["label"]

        try:
            sensortype.save()
            serializer = SensorTypeSerializer(sensortype, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        try:
            sensortype = SensorType.objects.get(pk=pk)
            serializer = SensorTypeSerializer(sensortype, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):

        sensortype = SensorType.objects.get(pk=pk)
        sensortype.label = request.data["label"]

        sensortype.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):

        try:
            sensortype = SensorType.objects.get(pk=pk)
            sensortype.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except SensorType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        tags = SensorType.objects.all()

        serializer = SensorTypeSerializer(
            tags, many=True, context={'request': request})
        return Response(serializer.data)
