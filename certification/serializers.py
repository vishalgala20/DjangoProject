from rest_framework import serializers
from .models import Certification


class CertificationSerializer(serializers.ModelSerializer):
    """Serializer for Certification model"""
    
    class Meta:
        model = Certification
        fields = ['id', 'name', 'code', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_code(self, value):
        """Validate that code is unique"""
        instance = self.instance
        if instance:
            if Certification.objects.filter(code=value).exclude(id=instance.id).exists():
                raise serializers.ValidationError("A certification with this code already exists.")
        else:
            if Certification.objects.filter(code=value).exists():
                raise serializers.ValidationError("A certification with this code already exists.")
        return value

    def validate_name(self, value):
        """Validate that name is not empty"""
        if not value or not str(value).strip():
            raise serializers.ValidationError("Name cannot be empty.")
        return value
