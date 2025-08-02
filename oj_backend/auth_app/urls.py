from django.urls import path
from .views import register_view, login_view, logout_view, problem_detail, problems_view, contests_view, submissions_view, leaderboard_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('problem/<int:problem_id>/', problem_detail, name='problem_detail'),
    path('problems/', problems_view, name='problems'),
    path('contests/', contests_view, name='contests'),
    path('submissions/', submissions_view, name='submissions'),
    path('leaderboard/', leaderboard_view, name='leaderboard'),
]
