from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from homeiotapi.models import UserPreference, AppUser
from homeiotapi.serializers import UserPreferencesSerializer

class UserPreferencesViewSet(ViewSet):

    def create(self, request):
        currentuser = AppUser.objects.get(user=request.auth.user)

        userpreference = UserPreference()
        userpreference.appuser = currentuser
        userpreference.unit = request.data["unit"]
        userpreference.fail_notification = request.data["fail_notification"]
        userpreference.threshold_notification = request.data["threshold_notification"]
        
        try:
            UserPreference.objects.get(appuser_id=currentuser.id)
        except UserPreference.DoesNotExist as ex:
            try:
                userpreference.save()
                serializer = UserPreferencesSerializer(userpreference, context={'request': request})
                return Response(serializer.data)

            except ValidationError as ex:
                return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as ex:
          return HttpResponseServerError(ex)
        
        return Response({"The user preferences for this user already exists"}, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk=None):
        try:
            userpreference = UserPreference.objects.get(pk=pk)
            serializer = UserPreferencesSerializer(userpreference, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):

        userpreference = UserPreference.objects.get(pk=pk)
        userpreference.unit = request.data["unit"]
        userpreference.fail_notification = request.data["fail_notification"]
        userpreference.threshold_notification = request.data["threshold_notification"]

        userpreference.save()
        return Response({"the user preferences has been updated"}, status=status.HTTP_204_NO_CONTENT)

    # don't want the userpreferences should be deleted. if user wants to delete the userpreference they can just delete the user and it will cascade down.

    # def destroy(self, request, pk=None):

    #     try:
    #         userpreference = UserPreference.objects.get(pk=pk)
    #         userpreference.delete()

    #         return Response({}, status=status.HTTP_204_NO_CONTENT)

    #     except UserPreference.DoesNotExist as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    #     except Exception as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        tags = UserPreference.objects.all()

        serializer = UserPreferencesSerializer(
            tags, many=True, context={'request': request})
        return Response(serializer.data)
