from django.urls import path
from .views import *

# app_name = "root"

urlpatterns = [
    path("test", test, name="test"),

]
