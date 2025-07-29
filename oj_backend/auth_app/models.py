from django.db import models

# Create your models here.

class Problem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(max_length=50, choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')])

    def __str__(self):
        return self.title
