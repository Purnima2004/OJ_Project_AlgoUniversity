from django.urls import path
from . import views

urlpatterns = [
    path('api/ai_review/', views.ai_review, name='ai_review'),
]
