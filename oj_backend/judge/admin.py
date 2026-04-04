from django.contrib import admin
from .models import Problem, TestCase, Contest, ContestParticipation


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'difficulty', 'created_at']
    list_filter = ['difficulty', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['id']


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'problem', 'is_sample', 'order']
    list_filter = ['is_sample', 'problem']
    ordering = ['problem', 'order']


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'is_active', 'start_date', 'end_date']
    list_filter = ['is_active', 'start_date', 'end_date']
    search_fields = ['title', 'description']


@admin.register(ContestParticipation)
class ContestParticipationAdmin(admin.ModelAdmin):
    list_display = ['user', 'contest', 'is_active', 'start_time', 'end_time']
    list_filter = ['is_active', 'contest']
    search_fields = ['user__username', 'contest__title']
