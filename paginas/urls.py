from django.contrib import admin
from django.urls import path, include
# from django.contrib.auth import views as auth_views
# from cars.views import CarsView, NewCarView
# from cars.views import CarsListView, NewCarCreateView
from .views import DashboardView

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # path('new_car/', NewCarCreateView.as_view(), name='new_car'),
]