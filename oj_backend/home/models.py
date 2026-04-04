from django.db import models


class ConceptOfDay(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    example_code = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'auth_app_conceptofday'

    def __str__(self):
        return self.title
