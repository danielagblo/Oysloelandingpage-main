from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/data/', views.api_data, name='api_data'),
]
