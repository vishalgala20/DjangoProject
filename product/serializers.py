from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model"""
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'code', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_code(self, value):
        """Validate that code is unique"""
        instance = self.instance
        if instance:
            if Product.objects.filter(code=value).exclude(id=instance.id).exists():
                raise serializers.ValidationError("A product with this code already exists.")
        else:
            if Product.objects.filter(code=value).exists():
                raise serializers.ValidationError("A product with this code already exists.")
        return value

    def validate_name(self, value):
        """Validate that name is not empty"""
        if not value or not str(value).strip():
            raise serializers.ValidationError("Name cannot be empty.")
        return value
