from django.urls import path
from . import views

urlpatterns = [
    path('compiler/', views.compiler_view, name='compiler'),
    path('compiler/run/', views.run_code, name='run_code'),
    path('compiler/submission/<str:submission_id>/', views.submission_detail, name='compiler_submission_detail'),
    path('compiler/my-submissions/', views.my_submissions, name='my_submissions'),
]
