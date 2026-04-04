"""
URL configuration for oj_backend project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home app – root and /home/
    path('', include('home.urls')),
    path('home/', include('home.urls')),

    # Auth (accounts)
    path('', include('accounts.urls')),

    # Online Judge
    path('', include('judge.urls')),

    # Standalone Compiler
    path('', include('compiler.urls')),

    # AI Review
    path('', include('ai_review.urls')),
]
