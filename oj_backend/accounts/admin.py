from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'score', 'rank', 'problems_solved_count']
    list_filter = ['rank']
    search_fields = ['user__username', 'user__email']

    def problems_solved_count(self, obj):
        return obj.problems_solved.count()
    problems_solved_count.short_description = 'Problems Solved'
