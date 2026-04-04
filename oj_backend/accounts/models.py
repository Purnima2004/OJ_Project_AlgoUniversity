from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    problems_solved = models.ManyToManyField(
        'judge.Problem', blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'auth_app_userprofile'

    def __str__(self):
        return f"{self.user.username}'s profile"
