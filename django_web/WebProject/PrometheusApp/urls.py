from django.urls import path, re_path
from django.views.generic import TemplateView
from . import views
from .views import get_metrics_ca, get_metrics_ne, get_metrics_we, get_metrics_energy, get_alerts, get_rules, get_container_alerts, get_container_rules
urlpatterns = [
  #USO API PROMETHEUS
    path("get_metrics_ne", get_metrics_ne, name='get_metrics_ne'),
    path("get_metrics_we", get_metrics_we, name='get_metrics_we'),
    path("get_metrics_ca", get_metrics_ca, name='get_metrics_ca'),
    path('get_metrics_energy', get_metrics_energy, name='get_metrics_energy'),
    path('get_alerts', get_alerts, name='get_alerts'),
    path('get_rules', get_rules, name='get_rules'),
    path('get_container_alerts', get_container_alerts, name='get_container_alerts'),
    path('get_container_rules', get_container_rules, name='get_container_rules'),
    
]