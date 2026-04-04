from django.db import models
from django.contrib.auth.models import User


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

    class Meta:
        db_table = 'auth_app_codesubmission'

    def __str__(self):
        return f"Submission {self.unique_id} - {self.language}"

    def save(self, *args, **kwargs):
        if not self.unique_id:
            import uuid
            self.unique_id = str(uuid.uuid4())
        super().save(*args, **kwargs)
