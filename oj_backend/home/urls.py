from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('landing/', views.home, name='landing'),
]
