from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Course
from .serializers import CourseSerializer


class CourseListCreateView(APIView):
    """
    API view for listing all courses and creating a new course.
    
    GET: Returns a list of all courses with pagination support
    POST: Creates a new course
    """

    @swagger_auto_schema(
        operation_description="Get list of all courses",
        manual_parameters=[
            openapi.Parameter(
                'is_active',
                openapi.IN_QUERY,
                description="Filter by is_active status (true/false)",
                type=openapi.TYPE_BOOLEAN
            ),
        ],
        responses={200: CourseSerializer(many=True)}
    )
    def get(self, request):
        """Retrieve list of courses with optional filtering"""
        queryset = Course.objects.all()
        
        # Filter by is_active if provided
        is_active = request.query_params.get('is_active', None)
        if is_active is not None:
            is_active = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active)
        
        serializer = CourseSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new course",
        request_body=CourseSerializer,
        responses={201: CourseSerializer, 400: "Bad Request"}
    )
    def post(self, request):
        """Create a new course"""
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailView(APIView):
    """
    API view for retrieving, updating and deleting a specific course.
    
    GET: Returns a specific course by id
    PUT: Updates a specific course (full update)
    PATCH: Partially updates a specific course
    DELETE: Deletes a specific course
    """

    def get_object(self, pk):
        """Helper method to get course by id"""
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Get a specific course by id",
        responses={200: CourseSerializer, 404: "Not Found"}
    )
    def get(self, request, pk):
        """Retrieve a specific course"""
        course = self.get_object(pk)
        if not course:
            return Response(
                {'error': 'Course not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update a specific course (full update)",
        request_body=CourseSerializer,
        responses={200: CourseSerializer, 400: "Bad Request", 404: "Not Found"}
    )
    def put(self, request, pk):
        """Full update a specific course"""
        course = self.get_object(pk)
        if not course:
            return Response(
                {'error': 'Course not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update a specific course",
        request_body=CourseSerializer,
        responses={200: CourseSerializer, 400: "Bad Request", 404: "Not Found"}
    )
    def patch(self, request, pk):
        """Partial update a specific course"""
        course = self.get_object(pk)
        if not course:
            return Response(
                {'error': 'Course not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a specific course",
        responses={204: "No Content", 404: "Not Found"}
    )
    def delete(self, request, pk):
        """Delete a specific course"""
        course = self.get_object(pk)
        if not course:
            return Response(
                {'error': 'Course not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
