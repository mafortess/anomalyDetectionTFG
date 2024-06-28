from django.urls import path
from . import views

urlpatterns = [
    path('scan_network/', views.scan_network, name='scan_network'),
   
   
    path('get_latest_capture/', views.get_latest_capture, name='get_latest_capture'),
   

    #Lista de capturas
    path('get_captures_by_ip/', views.get_captures_by_ip, name='get_captures_by_ip'),
    path('get_captures_by_table/', views.get_captures_table, name='get_captures_table'),
    
    #Una captura
    path('get_capture_by_ip/', views.get_capture_by_ip, name='get_capture_by_ip'),
    
    #Descarga captura
    path('download_tshark_capture/', views.download_tshark_capture, name='download_tshark_capture'),

     #Captura concreta
    path('tshark/', views.view_tshark_captures, name='view_tshark_captures'), 
    path('view_tshark_captures/', views.view_tshark_captures, name='view_tshark_captures'),


]
