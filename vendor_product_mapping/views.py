from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import VendorProductMapping
from .serializers import VendorProductMappingSerializer


class VendorProductMappingListCreateView(APIView):
    """
    API view for listing all vendor-product mappings and creating a new mapping.
    
    GET: Returns a list of all vendor-product mappings
    POST: Creates a new vendor-product mapping
    """

    @swagger_auto_schema(
        operation_description="Get list of all vendor-product mappings",
        manual_parameters=[
            openapi.Parameter(
                'vendor_id',
                openapi.IN_QUERY,
                description="Filter by vendor_id",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'product_id',
                openapi.IN_QUERY,
                description="Filter by product_id",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'primary_mapping',
                openapi.IN_QUERY,
                description="Filter by primary_mapping status (true/false)",
                type=openapi.TYPE_BOOLEAN
            ),
        ],
        responses={200: VendorProductMappingSerializer(many=True)}
    )
    def get(self, request):
        """Retrieve list of vendor-product mappings with optional filtering"""
        queryset = VendorProductMapping.objects.all()

        # Filter by vendor_id if provided
        vendor_id = request.query_params.get('vendor_id', None)
        if vendor_id:
            queryset = queryset.filter(vendor_id=vendor_id)

        # Filter by product_id if provided
        product_id = request.query_params.get('product_id', None)
        if product_id:
            queryset = queryset.filter(product_id=product_id)

        # Filter by primary_mapping if provided
        primary_mapping = request.query_params.get('primary_mapping', None)
        if primary_mapping is not None:
            primary_mapping = primary_mapping.lower() == 'true'
            queryset = queryset.filter(primary_mapping=primary_mapping)

        serializer = VendorProductMappingSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new vendor-product mapping",
        request_body=VendorProductMappingSerializer,
        responses={201: VendorProductMappingSerializer, 400: "Bad Request"}
    )
    def post(self, request):
        """Create a new vendor-product mapping"""
        serializer = VendorProductMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorProductMappingDetailView(APIView):
    """
    API view for retrieving, updating and deleting a specific vendor-product mapping.
    
    GET: Returns a specific mapping by id
    PUT: Updates a specific mapping (full update)
    PATCH: Partially updates a specific mapping
    DELETE: Deletes a specific mapping
    """

    def get_object(self, pk):
        """Helper method to get mapping by id"""
        try:
            return VendorProductMapping.objects.get(pk=pk)
        except VendorProductMapping.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Get a specific vendor-product mapping by id",
        responses={200: VendorProductMappingSerializer, 404: "Not Found"}
    )
    def get(self, request, pk):
        """Retrieve a specific vendor-product mapping"""
        mapping = self.get_object(pk)
        if not mapping:
            return Response(
                {'error': 'Vendor-Product mapping not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = VendorProductMappingSerializer(mapping)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update a specific vendor-product mapping (full update)",
        request_body=VendorProductMappingSerializer,
        responses={200: VendorProductMappingSerializer, 400: "Bad Request", 404: "Not Found"}
    )
    def put(self, request, pk):
        """Full update a specific vendor-product mapping"""
        mapping = self.get_object(pk)
        if not mapping:
            return Response(
                {'error': 'Vendor-Product mapping not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = VendorProductMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update a specific vendor-product mapping",
        request_body=VendorProductMappingSerializer,
        responses={200: VendorProductMappingSerializer, 400: "Bad Request", 404: "Not Found"}
    )
    def patch(self, request, pk):
        """Partial update a specific vendor-product mapping"""
        mapping = self.get_object(pk)
        if not mapping:
            return Response(
                {'error': 'Vendor-Product mapping not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = VendorProductMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a specific vendor-product mapping",
        responses={204: "No Content", 404: "Not Found"}
    )
    def delete(self, request, pk):
        """Delete a specific vendor-product mapping"""
        mapping = self.get_object(pk)
        if not mapping:
            return Response(
                {'error': 'Vendor-Product mapping not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
