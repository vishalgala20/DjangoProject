from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import ProductCourseMapping
from .serializers import ProductCourseMappingSerializer


class ProductCourseMappingListCreateView(APIView):
    """
    API view for listing all product-course mappings and creating a new mapping.
    
    GET: Returns a list of all product-course mappings
    POST: Creates a new product-course mapping
    """

    @swagger_auto_schema(
        operation_description="Get list of all product-course mappings",
        manual_parameters=[
            openapi.Parameter(
                'product_id',
                openapi.IN_QUERY,
                description="Filter by product_id",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'course_id',
                openapi.IN_QUERY,
                description="Filter by course_id",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'primary_mapping',
                openapi.IN_QUERY,
                description="Filter by primary_mapping status (true/false)",
                type=openapi.TYPE_BOOLEAN
            ),
        ],
        responses={200: ProductCourseMappingSerializer(many=True)}
    )
    def get(self, request):
        """Retrieve list of product-course mappings with optional filtering"""
        queryset = ProductCourseMapping.objects.all()

        # Filter by product_id if provided
        product_id = request.query_params.get('product_id', None)
        if product_id:
            queryset = queryset.filter(product_id=product_id)

        # Filter by course_id if provided
        course_id = request.query_params.get('course_id', None)
        if course_id:
            queryset = queryset.filter(course_id=course_id)

        # Filter by primary_mapping if provided
        primary_mapping = request.query_params.get('primary_mapping', None)
        if primary_mapping is not None:
            primary_mapping = primary_mapping.lower() == 'true'
            queryset = queryset.filter(primary_mapping=primary_mapping)

        serializer = ProductCourseMappingSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new product-course mapping",
        request_body=ProductCourseMappingSerializer,
        responses={201: ProductCourseMappingSerializer, 400: "Bad Request"}
    )
    def post(self, request):
        """Create a new product-course mapping"""
        serializer = ProductCourseMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductCourseMappingDetailView(APIView):
    """
    API view for retrieving, updating and deleting a specific product-course mapping.
    
    GET: Returns a specific mapping by id
    PUT: Updates a specific mapping (full update)
    PATCH: Partially updates a specific mapping
    DELETE: Deletes a specific mapping
    """

    def get_object(self, pk):
        """Helper method to get mapping by id"""
        try:
            return ProductCourseMapping.objects.get(pk=pk)
        except ProductCourseMapping.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Get a specific product-course mapping by id",
        responses={200: ProductCourseMappingSerializer, 404: "Not Found"}
    )
    def get(self, request, pk):
        """Retrieve a specific product-course mapping"""
        mapping = self.get_object(pk)
        if not mapping:
            return Response(
                {'error': 'Product-Course mapping not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductCourseMappingSerializer(mapping)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update a specific product-course mapping (full update)",
        request_body=ProductCourseMappingSerializer,
        responses={200: ProductCourseMappingSerializer, 400: "Bad Request", 404: "Not Found"}
    )
    def put(self, request, pk):
        """Full update a specific product-course mapping"""
        mapping = self.get_object(pk)
        if not mapping:
            return Response(
                {'error': 'Product-Course mapping not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductCourseMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update a specific product-course mapping",
        request_body=ProductCourseMappingSerializer,
        responses={200: ProductCourseMappingSerializer, 400: "Bad Request", 404: "Not Found"}
    )
    def patch(self, request, pk):
        """Partial update a specific product-course mapping"""
        mapping = self.get_object(pk)
        if not mapping:
            return Response(
                {'error': 'Product-Course mapping not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductCourseMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a specific product-course mapping",
        responses={204: "No Content", 404: "Not Found"}
    )
    def delete(self, request, pk):
        """Delete a specific product-course mapping"""
        mapping = self.get_object(pk)
        if not mapping:
            return Response(
                {'error': 'Product-Course mapping not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
