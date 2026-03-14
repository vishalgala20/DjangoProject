from rest_framework import serializers
from .models import ProductCourseMapping
from product.models import Product
from course.models import Course


class ProductCourseMappingSerializer(serializers.ModelSerializer):
    """Serializer for ProductCourseMapping model"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    
    class Meta:
        model = ProductCourseMapping
        fields = ['id', 'product', 'product_name', 'course', 'course_name', 'primary_mapping', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        """Validate that product and course exist, and duplicate mappings are prevented"""
        product = data.get('product')
        course = data.get('course')
        instance = self.instance

        # Validate that product exists
        if product and not Product.objects.filter(id=product.id).exists():
            raise serializers.ValidationError({'product': 'Product does not exist.'})

        # Validate that course exists
        if course and not Course.objects.filter(id=course.id).exists():
            raise serializers.ValidationError({'course': 'Course does not exist.'})

        # Check for duplicate mappings (same product-course pair)
        if product and course:
            existing = ProductCourseMapping.objects.filter(product=product, course=course)
            if instance:
                existing = existing.exclude(id=instance.id)
            if existing.exists():
                raise serializers.ValidationError(
                    "This product-course mapping already exists."
                )

        # Validate primary_mapping constraint
        if data.get('primary_mapping', False):
            primary_mapping = data.get('primary_mapping')
            if primary_mapping and product:
                existing_primary = ProductCourseMapping.objects.filter(
                    product=product,
                    primary_mapping=True
                )
                if instance:
                    existing_primary = existing_primary.exclude(id=instance.id)
                if existing_primary.exists():
                    raise serializers.ValidationError(
                        {'primary_mapping': 'Only one primary mapping can exist per product.'}
                    )

        return data

    def validate_product(self, value):
        """Validate that product is provided"""
        if not value:
            raise serializers.ValidationError("Product is required.")
        return value

    def validate_course(self, value):
        """Validate that course is provided"""
        if not value:
            raise serializers.ValidationError("Course is required.")
        return value
