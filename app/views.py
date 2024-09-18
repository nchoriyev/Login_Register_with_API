import requests
from django.shortcuts import render, redirect, reverse
from django.views import View
from .forms import RegisterForm, LoginForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages


class HomePageView(View):
    def get(self, request):
        access_token = request.COOKIES.get('access_token')

        if not access_token:
            return HttpResponseRedirect('login')
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        response = requests.get('http://127.0.0.2:8002/auth/token/verify', headers=headers)

        if response.status_code == 200:
            return HttpResponse("Siz tizimga kirdingiz va ushbu sahifaga kirishingiz mumkin!")
        elif response.status_code == 401:
            response = HttpResponseRedirect('/login/')
            response.delete_cookie('access_token')
            return response
        else:
            return HttpResponse("Noma'lum xato yuz berdi", status=500)


class RegisterPageView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            url = "http://127.0.0.2:8002/auth/register"
            data = {
                "username": form.cleaned_data['username'],
                "email": form.cleaned_data['email'],
                "password": form.cleaned_data['password']
            }
            response = requests.post(url, json=data)
            print(response.json())
            if response.json()["status_code"] == 201:
                return HttpResponse("User registered successfully")

            else:
                return HttpResponse(f"Error: {response.json()['detail']}")

        else:
            return HttpResponse("Form is not valid")


class LoginPageView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            url = "http://127.0.0.2:8002/auth/login"
            data = {
                "username_or_email": form.cleaned_data['username_or_email'],
                "password": form.cleaned_data['password']
            }
            response = requests.post(url, json=data)

            if response.json()["status_code"] == 200:
                access_token = response.json()['access_token']

                response = redirect('home')
                response.set_cookie('access_token', access_token, httponly=True)
                return response
            else:
                messages.error(request, "Invalid login credentials")

        return render(request, 'login.html')
