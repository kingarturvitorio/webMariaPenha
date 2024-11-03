from django.contrib import admin
from django.urls import path, include
# from django.contrib.auth import views as auth_views
# from cars.views import CarsView, NewCarView
from ocorrencia.views import OcorrenciaListView, OcorrenciaTabelaListView, OcorrenciaCreate
#, OcorrenciaUpdate, OcorrenciaDelete

urlpatterns = [
    path('listar_ocorrencia/', OcorrenciaListView.as_view(), name='ocorrencia-list'),
    path('ocorrencia/', OcorrenciaTabelaListView.as_view(), name='ocorrencia'),
    path('criar_ocorrencia/', OcorrenciaCreate.as_view(), name='ocorrencia-create'),
    # path('atualizar_ocorrencia/<int:pk>/', OcorrenciaUpdate.as_view(), name='ocorrencia-update'),
    # path('deletar_ocorrencia/<int:pk>/', OcorrenciaDelete.as_view(), name='ocorrencia-delete'),
    
    # path('new_car/', NewCarCreateView.as_view(), name='new_car'),
]