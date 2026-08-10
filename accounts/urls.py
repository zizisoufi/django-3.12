from django.urls import path
from .views import *


app_name = "accounts"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", logout_view, name="logout"),
    path("change-password/", change_password_view, name="change_password"),
    path("reset-password/", reset_password, name="reset_password"),
    path("reset-password-done/", reset_password_done, name="reset-password-done"),
    path("reset-password-confirm/<str:token>", reset_password_confirm, name="reset-password-confirm"),
    path("reset-password-complete/", reset_password_complete, name="reset-password-complete"),
]
    
