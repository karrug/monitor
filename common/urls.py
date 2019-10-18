from django.urls import path, include
from common.views import *

urlpatterns = [
    path("", index, name="index"),
    path("screenshot", screenshot, name="screenshot"),
    path("screenshot", screenshot, name="screenshot"),
]
