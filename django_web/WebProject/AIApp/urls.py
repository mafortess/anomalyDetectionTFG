from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import collect_data_view, train_model, evaluate_model, detect_anomalies

urlpatterns = [
    path('get_data/', views.collect_data_view, name='get_data'),
    path('collect_data/', collect_data_view, name='collect_data'),
    path('train_model/', train_model, name='train_model'),
    path('evaluate_model/', evaluate_model, name='evaluate_model'),
    path('detect_anomalies/', detect_anomalies, name='detect_anomalies'),   
    path('historial_anomalies/', views.historial_anomalias_view, name='historial_anomalias'), 
    path('toggle_monitoring/', views.toggle_monitoring, name='toggle_monitoring'),
    path('get_monitoring_state/', views.get_monitoring_state_view, name='get_monitoring_state'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)