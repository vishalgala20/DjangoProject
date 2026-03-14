from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import CourseCertificationMapping
from .serializers import CourseCertificationMappingSerializer


class CourseCertificationMappingListCreateView(APIView):
    """
    API view for listing all course-certification mappings and creating a new mapping.
    
    GET: Returns a list of all course-certification mappings
    POST: Creates a new course-certification mapping
    """

    @swagger_auto_schema(
        operation_description="Get list of all course-certification mappings",
        manual_parameters=[
            openapi.Parameter(
                'course_id',
                openapi.IN_QUERY,
                description="Filter by course_id",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'certification_id',
                openapi.IN_QUERY,
                description="Filter by certification_id",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'primary_mapping',
                openapi.IN_QUERY,
                description="Filter by primary_mapping status (true/false)",
                type=openapi.TYPE_BOOLEAN
            ),
        ],
        responses={200: CourseCertificationMappingSerializer(many=True)}
    )
    def get(self, request):
        """Retrieve list of course-certification mappings with optional filtering"""
        queryset = CourseCertificationMapping.objects.all()

        # Filter by course_id if provided
        course_id = request.query_params.get('course_id', None)
        if course_id:
            queryset = queryset.filter(course_id=course_id)

        # Filter by certification_id if provided
        certification_id = request.query_params.get('certification_id', None)
        if certification_id:
            queryset = queryset.filter(certification_id=certification_id)

        # Filter by primary_mapping if provided
        primary_mapping = request.query_params.get('primary_mapping', None)
        if primary_mapping is not None:
            primary_mapping = primary_mapping.lower() == 'true'
            queryset = queryset.filter(primary_mapping=primary_mapping)

        serializer = CourseCertificationMappingSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new course-certification mapping",
        request_body=CourseCertificationMappingSerializer,
        responses={201: CourseCertificationMappingSerializer, 400: "Bad Request"}
    )
    def post(self, request):
        """Create a new course-certification mapping"""
        serializer = CourseCertificationMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseCertificationMappingDetailView(APIView):
    """
    API view for retrieving, updating and deleting a specific course-certification mapping.
    
    GET: Returns a specific mapping by id
    PUT: Updates a specific mapping (full update)
    PATCH: Partially updates a specific mapping
    DELETE: Deletes a specific mapping
    """

    def get_object(self, pk):
        """Helper method to get mapping by id"""
        try:
            return CourseCertificationMapping.objects.get(pk=pk)
        except CourseCertificationMapping.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Get a specific course-certification mapping by id",
        responses={200: CourseCertificationMappingSerializer, 404: "Not Found"}
    )
    def get(self, request, pk):
        """Retrieve a specific course-certification mapping"""
        mapping = self.get_object(pk)
        if not mapping:
            return Response(
                {'error': 'Course-Certification mapping not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CourseCertificationMappingSerializer(mapping)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update a specific course-certification mapping (full update)",
        request_body=CourseCertificationMappingSerializer,
        responses={200: CourseCertificationMappingSerializer, 400: "Bad Request", 404: "Not Found"}
    )
    def put(self, request, pk):
        """Full update a specific course-certification mapping"""
        mapping = self.get_object(pk)
        if not mapping:
            return Response(
                {'error': 'Course-Certification mapping not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CourseCertificationMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update a specific course-certification mapping",
        request_body=CourseCertificationMappingSerializer,
        responses={200: CourseCertificationMappingSerializer, 400: "Bad Request", 404: "Not Found"}
    )
    def patch(self, request, pk):
        """Partial update a specific course-certification mapping"""
        mapping = self.get_object(pk)
        if not mapping:
            return Response(
                {'error': 'Course-Certification mapping not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CourseCertificationMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a specific course-certification mapping",
        responses={204: "No Content", 404: "Not Found"}
    )
    def delete(self, request, pk):
        """Delete a specific course-certification mapping"""
        mapping = self.get_object(pk)
        if not mapping:
            return Response(
                {'error': 'Course-Certification mapping not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
