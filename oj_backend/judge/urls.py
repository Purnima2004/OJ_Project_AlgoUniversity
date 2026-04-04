from django.urls import path
from . import views

urlpatterns = [
    # Problem URLs
    path('problems/', views.problems_view, name='problems'),
    path('problem/<int:problem_id>/', views.problem_detail, name='problem_detail'),
    path('problem/<int:problem_id>/submit/', views.submit_solution, name='submit_solution'),

    # Submission URLs
    path('submissions/', views.submissions_view, name='submissions'),
    path('submission/<int:submission_id>/', views.submission_detail_view, name='submission_detail'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    path('api/test-leaderboard/', views.test_leaderboard_data, name='test_leaderboard_data'),

    # Contest URLs
    path('contests/', views.contests_view, name='contests'),
    path('contest/<int:contest_id>/', views.contest_detail, name='contest_detail'),
    path('contest/<int:contest_id>/start/', views.start_contest, name='start_contest'),
    path('contest/<int:contest_id>/timer/', views.get_contest_timer, name='get_contest_timer'),
    path('contest/<int:contest_id>/end/', views.end_contest, name='end_contest'),

    # Admin URLs
    path('admin/create-problem/', views.create_problem, name='create_problem'),
    path('admin/create-contest/', views.create_contest, name='create_contest'),
    path('admin/problem/<int:problem_id>/test-cases/', views.manage_test_cases, name='manage_test_cases'),
    path('admin/create-sample-data/', views.create_sample_data, name='create_sample_data'),
]
