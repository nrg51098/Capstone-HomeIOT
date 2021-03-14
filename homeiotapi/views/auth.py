import json
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from homeiotapi.models import AppUser, UserPreference, appuser


@csrf_exempt
def register_user(request):

    # incoming Json string
    req_body = json.loads(request.body.decode())

    # check if user exists in db
    user_exists = User.objects.filter(email=req_body['email']).exists()

    if user_exists:
        data = json.dumps({"msg": "user already exists"})
        return HttpResponse(data, content_type='application/json')

    # invoke Djangos built in user model
    new_user = User.objects.create_user(
        username=req_body['username'],
        email=req_body['email'],
        password=req_body['password'],
        first_name=req_body['first_name'],
        last_name=req_body['last_name'],
        is_active=True,
        is_staff=False
    )

    # Add extra info to AppUser table
    appUser = AppUser.objects.create(
        address=req_body['address'],
        profile_img_url=req_body['profile_img_url'],
        user=new_user
    )

    # Commit the user to the database by saving it
    appUser.save()

    # Create default userpreferences for the new user automatially
    userpreference = UserPreference.objects.create(
        unit= "IN",
        fail_notification = False,
        threshold_notification = False,
        appuser=appUser
    )
    # Commit the user preference to the database by saving it
    userpreference.save()

    # Use the REST Framework's token generator on the new user account
    token = Token.objects.create(user=new_user)

    # Return the token to the client
    data = json.dumps({"token": token.key})
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def login_user(request):
    # the request data
    req_body = json.loads(request.body.decode())

    # Using Django native auth
    if request.method == 'POST':
        username = req_body['username']
        password = req_body['password']
        authenticated_user = authenticate(username=username, password=password)

        # If authentication was successful, respond with their token
        if authenticated_user is not None:

            try:
                token = Token.objects.get(user=authenticated_user)
                data = json.dumps({"valid": True, "token": token.key})
                return HttpResponse(data, content_type='application/json')
            except:
                print("There was a problem logging in the user")
                data = json.dumps(
                    {"valid": False, "msg": "There was a server error when logging in the user"})
                return HttpResponse(data, content_type='application/json')

        else:
            # Bad login details were provided. So we can't log the user in.
            data = json.dumps({"valid": False})
            return HttpResponse(data, content_type='application/json')


@csrf_exempt
def get_current_user(request):

    req_body = json.loads(request.body.decode())

    try:
        user_id = Token.objects.get(key=req_body['token']).user_id
        data = json.dumps({"user_id": user_id})
        return HttpResponse(data, content_type="application/json")
    except Token.DoesNotExist:
        data = json.dumps(
            {"valid": False, "msg": "No currently authenticated user."})
        return HttpResponse(data, content_type='application/json')


@csrf_exempt
def is_current_user_admin(request):

    req_body = json.loads(request.body.decode())

    try:
        user_id = Token.objects.get(key=req_body['token']).user_id
        is_admin = User.objects.get(pk=user_id).is_staff
        data = json.dumps({"is_user_admin": is_admin})
        return HttpResponse(data, content_type="application/json")
    except Token.DoesNotExist:
        data = json.dumps(
            {"valid": False, "msg": "No currently authenticated user."}
        )
        return HttpResponse(data, content_type="application/json")
