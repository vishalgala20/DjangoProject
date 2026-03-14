from rest_framework import serializers
from .models import CourseCertificationMapping
from course.models import Course
from certification.models import Certification


class CourseCertificationMappingSerializer(serializers.ModelSerializer):
    """Serializer for CourseCertificationMapping model"""
    course_name = serializers.CharField(source='course.name', read_only=True)
    certification_name = serializers.CharField(source='certification.name', read_only=True)
    
    class Meta:
        model = CourseCertificationMapping
        fields = ['id', 'course', 'course_name', 'certification', 'certification_name', 'primary_mapping', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        """Validate that course and certification exist, and duplicate mappings are prevented"""
        course = data.get('course')
        certification = data.get('certification')
        instance = self.instance

        # Validate that course exists
        if course and not Course.objects.filter(id=course.id).exists():
            raise serializers.ValidationError({'course': 'Course does not exist.'})

        # Validate that certification exists
        if certification and not Certification.objects.filter(id=certification.id).exists():
            raise serializers.ValidationError({'certification': 'Certification does not exist.'})

        # Check for duplicate mappings (same course-certification pair)
        if course and certification:
            existing = CourseCertificationMapping.objects.filter(course=course, certification=certification)
            if instance:
                existing = existing.exclude(id=instance.id)
            if existing.exists():
                raise serializers.ValidationError(
                    "This course-certification mapping already exists."
                )

        # Validate primary_mapping constraint
        if data.get('primary_mapping', False):
            primary_mapping = data.get('primary_mapping')
            if primary_mapping and course:
                existing_primary = CourseCertificationMapping.objects.filter(
                    course=course,
                    primary_mapping=True
                )
                if instance:
                    existing_primary = existing_primary.exclude(id=instance.id)
                if existing_primary.exists():
                    raise serializers.ValidationError(
                        {'primary_mapping': 'Only one primary mapping can exist per course.'}
                    )

        return data

    def validate_course(self, value):
        """Validate that course is provided"""
        if not value:
            raise serializers.ValidationError("Course is required.")
        return value

    def validate_certification(self, value):
        """Validate that certification is provided"""
        if not value:
            raise serializers.ValidationError("Certification is required.")
        return value
