from django.urls import path

from . import views

app_name = "boxes"

urlpatterns = [
    path("", views.home, name="home"),
    path("size-chart/", views.size_chart, name="size_chart"),
]
