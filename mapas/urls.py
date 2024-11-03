# urls.py
from django.urls import path
from .views import mapa_view, send_coordinates

urlpatterns = [
    path('mapa/', mapa_view, name='mapa'),
    path('api/send-coordinates/', send_coordinates, name='send_coordinates'),
]