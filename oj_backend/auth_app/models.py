from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Problem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(max_length=50, choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')])
    test_cases = models.TextField(blank=True)
    examples = models.TextField(blank=True)
    constraints = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Contest(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    problems = models.ManyToManyField(Problem, blank=True)
    
    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    problems_solved = models.ManyToManyField(Problem, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - Score: {self.score}"

class Submission(models.Model):
    STATUS_CHOICES = [
        ('AC', 'Accepted'),
        ('WA', 'Wrong Answer'),
        ('TLE', 'Time Limit Exceeded'),
        ('RE', 'Runtime Error'),
        ('CE', 'Compilation Error'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, null=True, blank=True)
    code = models.TextField()
    language = models.CharField(max_length=20, choices=[
        ('python', 'Python'),
        ('cpp', 'C++'),
        ('java', 'Java'),
    ], default='python')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    submitted_at = models.DateTimeField(default=timezone.now)
    execution_time = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.problem.title} - {self.status}"

class ConceptOfDay(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    concept_type = models.CharField(max_length=50, default='DP')
    date = models.DateField(unique=True)
    example_code = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.date}"
