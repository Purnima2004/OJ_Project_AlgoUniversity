from django.urls import path
from .views import (
    register_view, login_view, logout_view, home,
    problem_detail, problems_view, contests_view, submissions_view, leaderboard_view,
    submit_solution, submission_detail_view, contest_detail,
    create_problem, create_contest, manage_test_cases, create_sample_data,
    compiler_view, run_code, submission_detail, my_submissions,
    start_contest, get_contest_timer, end_contest, ai_review
)

urlpatterns = [
    path('', home, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    # Problem and Contest URLs
    path('problems/', problems_view, name='problems'),
    path('problem/<int:problem_id>/', problem_detail, name='problem_detail'),
    path('problem/<int:problem_id>/submit/', submit_solution, name='submit_solution'),
    path('contests/', contests_view, name='contests'),
    path('contest/<int:contest_id>/', contest_detail, name='contest_detail'),
    path('contest/<int:contest_id>/start/', start_contest, name='start_contest'),
    path('contest/<int:contest_id>/timer/', get_contest_timer, name='get_contest_timer'),
    path('contest/<int:contest_id>/end/', end_contest, name='end_contest'),
    
    # Submission URLs
    path('submissions/', submissions_view, name='submissions'),
    path('submission/<int:submission_id>/', submission_detail_view, name='submission_detail'),
    path('leaderboard/', leaderboard_view, name='leaderboard'),
    
    # Admin URLs
    path('admin/create-problem/', create_problem, name='create_problem'),
    path('admin/create-contest/', create_contest, name='create_contest'),
    path('admin/problem/<int:problem_id>/test-cases/', manage_test_cases, name='manage_test_cases'),
    path('admin/create-sample-data/', create_sample_data, name='create_sample_data'),
    
    # Compiler URLs
    path('compiler/', compiler_view, name='compiler'),
    path('compiler/run/', run_code, name='run_code'),
    path('compiler/submission/<str:submission_id>/', submission_detail, name='submission_detail'),
    path('compiler/my-submissions/', my_submissions, name='my_submissions'),
    
    # AI Review URL
    path('api/ai_review/', ai_review, name='ai_review'),
]
