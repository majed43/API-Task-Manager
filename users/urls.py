from django.urls import path

from .views import EmailAuthToken, register, search, update_password, update_profile

urlpatterns = [
    path("register/", register),
    path("update/", update_profile),
    path("update-password/", update_password),
    path("login/", EmailAuthToken.as_view()),
    path("<str:username>/", search),
]
