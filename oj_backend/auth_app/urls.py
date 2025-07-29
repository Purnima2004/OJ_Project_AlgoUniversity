from django.urls import path
from .views import register_view, login_view, logout_view, problem_detail

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('problem/<int:problem_id>/', problem_detail, name='problem_detail'),
]
