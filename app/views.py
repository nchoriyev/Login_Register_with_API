from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from .forms import UserRegisterForm, UserLoginForm
import requests

class HomePageVew(View):
    def get(self, request):
        return render(request, 'home.html')

class RegisterPageView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'register.html', {"form": form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            url = 'http://localhost:8001/auth/register'
            data = {
                "username": username,
                "email": email,
                "password": password
            }
            response = requests.post(url, json=data)
            if response.status_code == 200:
                return HttpResponse("User registered successfully!")
            else:
                return HttpResponse(f"Error: {response.json()['detail']}")
        else:
            form = UserRegisterForm()
            return render(request, 'register.html', {'form': form})

class LoginPageView(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, 'login.html', {"form": form})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            url = 'http://localhost:8001/auth/login'
            data = {
                "username": username,
                "password": password
            }
            response = requests.post(url, json=data)
            if response.status_code == 200:
                token = response.json().get('access')
                # Store the token in session or cookies if necessary
                request.session['auth_token'] = token
                return redirect('home')  # Redirect to the homepage or dashboard
            else:
                return HttpResponse(f"Login failed: {response.json()['detail']}")
        else:
            return render(request, 'login.html', {'form': form})
