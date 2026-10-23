from django.urls import path

from . import views

app_name = "boxes"

urlpatterns = [
    path("", views.home, name="home"),
]
