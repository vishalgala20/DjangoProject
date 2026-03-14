from django.db import models
from django.core.exceptions import ValidationError
from vendor.models import Vendor
from product.models import Product


class VendorProductMapping(models.Model):
    """Mapping between Vendor and Product"""
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='product_mappings')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='vendor_mappings')
    primary_mapping = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'vendor_product_mapping'
        unique_together = ['vendor', 'product']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.vendor.name} -> {self.product.name}"

    def clean(self):
        """Validate that only one primary mapping exists per vendor"""
        if self.primary_mapping:
            existing_primary = VendorProductMapping.objects.filter(
                vendor=self.vendor,
                primary_mapping=True
            ).exclude(id=self.id)
            if existing_primary.exists():
                raise ValidationError(
                    "Only one primary mapping can exist per vendor. "
                    f"Vendor {self.vendor.name} already has a primary product mapping."
                )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
