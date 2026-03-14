from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Product
from .serializers import ProductSerializer


class ProductListCreateView(APIView):
    """
    API view for listing all products and creating a new product.
    
    GET: Returns a list of all products with pagination support
    POST: Creates a new product
    """

    @swagger_auto_schema(
        operation_description="Get list of all products",
        manual_parameters=[
            openapi.Parameter(
                'is_active',
                openapi.IN_QUERY,
                description="Filter by is_active status (true/false)",
                type=openapi.TYPE_BOOLEAN
            ),
        ],
        responses={200: ProductSerializer(many=True)}
    )
    def get(self, request):
        """Retrieve list of products with optional filtering"""
        queryset = Product.objects.all()
        
        # Filter by is_active if provided
        is_active = request.query_params.get('is_active', None)
        if is_active is not None:
            is_active = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active)
        
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new product",
        request_body=ProductSerializer,
        responses={201: ProductSerializer, 400: "Bad Request"}
    )
    def post(self, request):
        """Create a new product"""
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    """
    API view for retrieving, updating and deleting a specific product.
    
    GET: Returns a specific product by id
    PUT: Updates a specific product (full update)
    PATCH: Partially updates a specific product
    DELETE: Deletes a specific product
    """

    def get_object(self, pk):
        """Helper method to get product by id"""
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Get a specific product by id",
        responses={200: ProductSerializer, 404: "Not Found"}
    )
    def get(self, request, pk):
        """Retrieve a specific product"""
        product = self.get_object(pk)
        if not product:
            return Response(
                {'error': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update a specific product (full update)",
        request_body=ProductSerializer,
        responses={200: ProductSerializer, 400: "Bad Request", 404: "Not Found"}
    )
    def put(self, request, pk):
        """Full update a specific product"""
        product = self.get_object(pk)
        if not product:
            return Response(
                {'error': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update a specific product",
        request_body=ProductSerializer,
        responses={200: ProductSerializer, 400: "Bad Request", 404: "Not Found"}
    )
    def patch(self, request, pk):
        """Partial update a specific product"""
        product = self.get_object(pk)
        if not product:
            return Response(
                {'error': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a specific product",
        responses={204: "No Content", 404: "Not Found"}
    )
    def delete(self, request, pk):
        """Delete a specific product"""
        product = self.get_object(pk)
        if not product:
            return Response(
                {'error': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
