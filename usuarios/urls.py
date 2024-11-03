from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_view, login_view, logout_view


urlpatterns = [
    path('', login_view, name='login'), 
    path('register/', register_view, name='register'), 
    path('logout/', logout_view, name='logout'), 

    # path('new_car/', NewCarCreateView.as_view(), name='new_car'),
]