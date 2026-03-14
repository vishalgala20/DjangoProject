from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Vendor
from .serializers import VendorSerializer


class VendorListCreateView(APIView):
    """
    API view for listing all vendors and creating a new vendor.
    
    GET: Returns a list of all vendors with pagination support
    POST: Creates a new vendor
    """

    @swagger_auto_schema(
        operation_description="Get list of all vendors",
        manual_parameters=[
            openapi.Parameter(
                'is_active',
                openapi.IN_QUERY,
                description="Filter by is_active status (true/false)",
                type=openapi.TYPE_BOOLEAN
            ),
        ],
        responses={200: VendorSerializer(many=True)}
    )
    def get(self, request):
        """Retrieve list of vendors with optional filtering"""
        queryset = Vendor.objects.all()
        
        # Filter by is_active if provided
        is_active = request.query_params.get('is_active', None)
        if is_active is not None:
            is_active = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active)
        
        serializer = VendorSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new vendor",
        request_body=VendorSerializer,
        responses={201: VendorSerializer, 400: "Bad Request"}
    )
    def post(self, request):
        """Create a new vendor"""
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorDetailView(APIView):
    """
    API view for retrieving, updating and deleting a specific vendor.
    
    GET: Returns a specific vendor by id
    PUT: Updates a specific vendor (full update)
    PATCH: Partially updates a specific vendor
    DELETE: Deletes a specific vendor
    """

    def get_object(self, pk):
        """Helper method to get vendor by id"""
        try:
            return Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Get a specific vendor by id",
        responses={200: VendorSerializer, 404: "Not Found"}
    )
    def get(self, request, pk):
        """Retrieve a specific vendor"""
        vendor = self.get_object(pk)
        if not vendor:
            return Response(
                {'error': 'Vendor not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = VendorSerializer(vendor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update a specific vendor (full update)",
        request_body=VendorSerializer,
        responses={200: VendorSerializer, 400: "Bad Request", 404: "Not Found"}
    )
    def put(self, request, pk):
        """Full update a specific vendor"""
        vendor = self.get_object(pk)
        if not vendor:
            return Response(
                {'error': 'Vendor not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update a specific vendor",
        request_body=VendorSerializer,
        responses={200: VendorSerializer, 400: "Bad Request", 404: "Not Found"}
    )
    def patch(self, request, pk):
        """Partial update a specific vendor"""
        vendor = self.get_object(pk)
        if not vendor:
            return Response(
                {'error': 'Vendor not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = VendorSerializer(vendor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a specific vendor",
        responses={204: "No Content", 404: "Not Found"}
    )
    def delete(self, request, pk):
        """Delete a specific vendor"""
        vendor = self.get_object(pk)
        if not vendor:
            return Response(
                {'error': 'Vendor not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
