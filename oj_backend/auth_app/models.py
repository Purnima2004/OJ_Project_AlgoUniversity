from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import json

class Problem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(max_length=50, choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')])
    examples = models.TextField(blank=True)
    constraints = models.TextField(blank=True)
    time_limit = models.IntegerField(default=1000)  # milliseconds
    memory_limit = models.IntegerField(default=256)  # MB
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='test_cases')
    input_data = models.TextField()
    expected_output = models.TextField()
    is_sample = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.problem.title} - Test Case {self.order}"

class Contest(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    problems = models.ManyToManyField(Problem, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def is_running(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date

    @property
    def has_started(self):
        return timezone.now() >= self.start_date

    @property
    def has_ended(self):
        return timezone.now() > self.end_date

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    problems_solved = models.ManyToManyField(Problem, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

class Submission(models.Model):
    STATUS_CHOICES = [
        ('AC', 'Accepted'),
        ('WA', 'Wrong Answer'),
        ('TLE', 'Time Limit Exceeded'),
        ('RE', 'Runtime Error'),
        ('CE', 'Compilation Error'),
        ('MLE', 'Memory Limit Exceeded'),
        ('PE', 'Presentation Error'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, null=True, blank=True)
    code = models.TextField()
    language = models.CharField(max_length=20, choices=[
        ('python', 'Python'), ('cpp', 'C++'), ('java', 'Java'),
    ], default='python')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='WA')
    execution_time = models.FloatField(null=True, blank=True)
    memory_used = models.IntegerField(null=True, blank=True)  # KB
    test_cases_passed = models.IntegerField(default=0)
    total_test_cases = models.IntegerField(default=0)
    error_message = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.user.username} - {self.problem.title} - {self.status}"

class SubmissionResult(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='results')
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=Submission.STATUS_CHOICES)
    execution_time = models.FloatField(null=True, blank=True)
    memory_used = models.IntegerField(null=True, blank=True)
    actual_output = models.TextField(blank=True)
    error_message = models.TextField(blank=True)

    def __str__(self):
        return f"{self.submission.id} - Test Case {self.test_case.order}"

class CodeSubmission(models.Model):
    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('cpp', 'C++'),
        ('java', 'Java'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='python')
    code = models.TextField()
    input_data = models.TextField(blank=True)
    output = models.TextField(blank=True)
    error_message = models.TextField(blank=True)
    execution_time = models.FloatField(null=True, blank=True)
    memory_used = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    unique_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Submission {self.unique_id} - {self.language}"

    def save(self, *args, **kwargs):
        if not self.unique_id:
            import uuid
            self.unique_id = str(uuid.uuid4())
        super().save(*args, **kwargs)

class ContestParticipation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(default=0)
    problems_solved = models.ManyToManyField(Problem, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['user', 'contest']
    
    def __str__(self):
        return f"{self.user.username} - {self.contest.title}"
    
    @property
    def time_remaining(self):
        """Get remaining time in seconds"""
        if not self.is_active:
            return 0
        
        # User has a fixed 90-minute window once they start
        personal_deadline = self.start_time + timedelta(minutes=90)
        # But never extend beyond contest's scheduled end
        contest_end = self.contest.end_date
        effective_deadline = min(personal_deadline, contest_end)
        now = timezone.now()
        if now >= effective_deadline:
            return 0
        return int((effective_deadline - now).total_seconds())
    
    @property
    def elapsed_time(self):
        """Get elapsed time in seconds"""
        if self.end_time:
            return int((self.end_time - self.start_time).total_seconds())
        else:
            return int((timezone.now() - self.start_time).total_seconds())

class ConceptOfDay(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    example_code = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
