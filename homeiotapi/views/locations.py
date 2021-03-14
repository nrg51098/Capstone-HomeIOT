from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from homeiotapi.models import Location
from homeiotapi.serializers import LocationSerializer

class LocationsViewSet(ViewSet):

    def create(self, request):

        location = Location()
        location.label = request.data["label"]

        try:
            location.save()
            serializer = LocationSerializer(location, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        try:
            location = Location.objects.get(pk=pk)
            serializer = LocationSerializer(location, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):

        location = Location.objects.get(pk=pk)
        location.label = request.data["label"]

        location.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):

        try:
            location = Location.objects.get(pk=pk)
            location.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Location.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        tags = Location.objects.all()

        serializer = LocationSerializer(
            tags, many=True, context={'request': request})
        return Response(serializer.data)
