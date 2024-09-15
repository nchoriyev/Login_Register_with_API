from django.urls import path
from .views import RegisterPageView, HomePageVew, LoginPageView

urlpatterns = [
    path('', HomePageVew.as_view(), name='home'),
    path('register/', RegisterPageView.as_view(), name='register'),
    path('login/', LoginPageView.as_view(), name='login'),
]