from django.contrib import admin
from django.urls import path, include
# from django.contrib.auth import views as auth_views
# from cars.views import CarsView, NewCarView
from registro.views import RegistroTabelaListView, RegistroCreateView, RegistroUpdateView, RegistroDeleteView

urlpatterns = [
    path('registro/', RegistroTabelaListView.as_view(), name='registro'),
    path('criar_registro/', RegistroCreateView.as_view(), name='registro-create'),
    path('atualizar_registro/<int:id>/', RegistroUpdateView.as_view(), name='registro-update'),
    path('deletar_registro/<int:id>/', RegistroDeleteView.as_view(), name='registro-delete'),
    
    # path('new_car/', NewCarCreateView.as_view(), name='new_car'),
]