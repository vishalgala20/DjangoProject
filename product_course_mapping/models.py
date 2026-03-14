from django.db import models
from django.core.exceptions import ValidationError
from product.models import Product
from course.models import Course


class ProductCourseMapping(models.Model):
    """Mapping between Product and Course"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='course_mappings')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='product_mappings')
    primary_mapping = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product_course_mapping'
        unique_together = ['product', 'course']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.name} -> {self.course.name}"

    def clean(self):
        """Validate that only one primary mapping exists per product"""
        if self.primary_mapping:
            existing_primary = ProductCourseMapping.objects.filter(
                product=self.product,
                primary_mapping=True
            ).exclude(id=self.id)
            if existing_primary.exists():
                raise ValidationError(
                    "Only one primary mapping can exist per product. "
                    f"Product {self.product.name} already has a primary course mapping."
                )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
