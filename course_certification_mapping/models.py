from django.db import models
from django.core.exceptions import ValidationError
from course.models import Course
from certification.models import Certification


class CourseCertificationMapping(models.Model):
    """Mapping between Course and Certification"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certification_mappings')
    certification = models.ForeignKey(Certification, on_delete=models.CASCADE, related_name='course_mappings')
    primary_mapping = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'course_certification_mapping'
        unique_together = ['course', 'certification']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.course.name} -> {self.certification.name}"

    def clean(self):
        """Validate that only one primary mapping exists per course"""
        if self.primary_mapping:
            existing_primary = CourseCertificationMapping.objects.filter(
                course=self.course,
                primary_mapping=True
            ).exclude(id=self.id)
            if existing_primary.exists():
                raise ValidationError(
                    "Only one primary mapping can exist per course. "
                    f"Course {self.course.name} already has a primary certification mapping."
                )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
