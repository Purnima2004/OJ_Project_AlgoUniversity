from django.urls import path
from .views import register_view, login_view, logout_view, problem_detail, problems_view, contests_view, submissions_view, leaderboard_view
from .compiler_views import compiler_view, run_code, submission_detail, my_submissions

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('problem/<int:problem_id>/', problem_detail, name='problem_detail'),
    path('problems/', problems_view, name='problems'),
    path('contests/', contests_view, name='contests'),
    path('submissions/', submissions_view, name='submissions'),
    path('leaderboard/', leaderboard_view, name='leaderboard'),
    
    # Compiler URLs
    path('compiler/', compiler_view, name='compiler'),
    path('compiler/run/', run_code, name='run_code'),
    path('compiler/submission/<str:submission_id>/', submission_detail, name='submission_detail'),
    path('compiler/my-submissions/', my_submissions, name='my_submissions'),
]
