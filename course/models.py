from django.db import models


class Course(models.Model):
    """Master Course entity"""
    name = models.CharField(max_length=255, unique=False, blank=False)
    code = models.CharField(max_length=100, unique=True, blank=False)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'course'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.code})"
