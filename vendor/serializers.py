from rest_framework import serializers
from .models import Vendor


class VendorSerializer(serializers.ModelSerializer):
    """Serializer for Vendor model"""
    
    class Meta:
        model = Vendor
        fields = ['id', 'name', 'code', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_code(self, value):
        """Validate that code is unique"""
        instance = self.instance
        if instance:
            if Vendor.objects.filter(code=value).exclude(id=instance.id).exists():
                raise serializers.ValidationError("A vendor with this code already exists.")
        else:
            if Vendor.objects.filter(code=value).exists():
                raise serializers.ValidationError("A vendor with this code already exists.")
        return value

    def validate_name(self, value):
        """Validate that name is not empty"""
        if not value or not str(value).strip():
            raise serializers.ValidationError("Name cannot be empty.")
        return value
