from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import action

from .forms import LoginForm


class LogUser(APIView):
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)

                return redirect('home')
                return HttpResponse(f"User {username} is LOGGED In")
            else:
                return HttpResponse(f"User: {username} does not match")
        return HttpResponse("Please Make the form correct")
    def get(self, request):
        form = LoginForm
        return render(request, 'index.html')
    
    @action(methods=['get'], detail=True)
    def getout(self, request):
        user = request.user
        print(f"The user sent is : {user}")
        return HttpResponse("You're correct")