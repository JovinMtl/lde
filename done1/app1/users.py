from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

from django.utils import timezone
from pytz import timezone as pytz_timezone

from .serializers import UserSeriazer, PorteSeria
from .models import PorteFeuille

from .lumi.client_Lumi import LumiRequest

""" I want to write views related to Users"""




   
@api_view(['POST', 'GET'])
def injira(request):
    """This is for logging in and out the user"""
    username = "None"
    if request.POST:
        sent_data = request.POST
        username = request.POST.get('username')
        password = sent_data['password']

        # print(f"the username sent is : {username}")

    user = authenticate(username=username, password=password)
    user = User.objects.get(username=username)
    # print(f"We are going to use the user: {user}")
    if user :
        login(request, user)
        return JsonResponse({'message': 'Login successful'})
    else:
        print(f"You need to provide a user: {user}")
        return JsonResponse({'message': 'Login failed'}, status=401)


def check_user_authenticated(request):
    if request.user.is_authenticated:
        return JsonResponse({'message': 'User is authenticated'})
    else:
        return JsonResponse({'message': 'User is not authenticated'},\
                             status=401)

def userTime(request):
    # Set the user's timezone preference in the session
    request.session['user_timezone'] = 'Etc/GMT-2'

    # Retrieve the user's timezone preference from the session
    user_timezone = request.session.get('user_timezone', 'UTC')

    # Activate the user's timezone
    user_tz = pytz_timezone(user_timezone)
    timezone.activate(user_tz)

    # Perform operations using the user's timezone preference
    # Example: Displaying the current time in the user's timezone
    current_time = timezone.localtime(timezone.now())

    return JsonResponse({"Timezone": current_time})
