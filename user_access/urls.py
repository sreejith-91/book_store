from django.urls import path

from user_access.views import *
app_name = "user_access"
urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('register', RegisterUserView.as_view(), name='register'),
]
