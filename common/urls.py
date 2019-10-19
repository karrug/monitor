from django.urls import path, include
from common.views import *

urlpatterns = [
    path("", index, name="index"),
    path("screenshot", screenshot, name="screenshot"),
    path("list/screenshots", list_screenshots, name="list_screenshots"),
]
