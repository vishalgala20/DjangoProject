from rest_framework import serializers
from .models import VendorProductMapping
from vendor.models import Vendor
from product.models import Product


class VendorProductMappingSerializer(serializers.ModelSerializer):
    """Serializer for VendorProductMapping model"""
    vendor_name = serializers.CharField(source='vendor.name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = VendorProductMapping
        fields = ['id', 'vendor', 'vendor_name', 'product', 'product_name', 'primary_mapping', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        """Validate that vendor and product exist, and duplicate mappings are prevented"""
        vendor = data.get('vendor')
        product = data.get('product')
        instance = self.instance

        # Validate that vendor exists
        if vendor and not Vendor.objects.filter(id=vendor.id).exists():
            raise serializers.ValidationError({'vendor': 'Vendor does not exist.'})

        # Validate that product exists
        if product and not Product.objects.filter(id=product.id).exists():
            raise serializers.ValidationError({'product': 'Product does not exist.'})

        # Check for duplicate mappings (same vendor-product pair)
        if vendor and product:
            existing = VendorProductMapping.objects.filter(vendor=vendor, product=product)
            if instance:
                existing = existing.exclude(id=instance.id)
            if existing.exists():
                raise serializers.ValidationError(
                    "This vendor-product mapping already exists."
                )

        # Validate primary_mapping constraint
        if data.get('primary_mapping', False):
            primary_mapping = data.get('primary_mapping')
            if primary_mapping and vendor:
                existing_primary = VendorProductMapping.objects.filter(
                    vendor=vendor,
                    primary_mapping=True
                )
                if instance:
                    existing_primary = existing_primary.exclude(id=instance.id)
                if existing_primary.exists():
                    raise serializers.ValidationError(
                        {'primary_mapping': 'Only one primary mapping can exist per vendor.'}
                    )

        return data

    def validate_vendor(self, value):
        """Validate that vendor is provided"""
        if not value:
            raise serializers.ValidationError("Vendor is required.")
        return value

    def validate_product(self, value):
        """Validate that product is provided"""
        if not value:
            raise serializers.ValidationError("Product is required.")
        return value
