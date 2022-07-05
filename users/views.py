# from django.shortcuts import render
from django.contrib.auth.views import LoginView

# Create your views here.
class UserLogin(LoginView):
    template_name = 'users/login.html'
