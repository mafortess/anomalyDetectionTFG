from django.urls import path, re_path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("host", views.hostdash, name="HostDashboard"),
    path('container', views.containerdash, name="ContainerDashboard"),
    path("aihost", views.aihostdash, name="AiHostDashboard"),   
    path("energyt", views.energytdash, name="EnergyTDashboard"),
    path("practdash", views.practdash, name="practdashboard"),
] 
