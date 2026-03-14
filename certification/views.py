from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Certification
from .serializers import CertificationSerializer


class CertificationListCreateView(APIView):
    """
    API view for listing all certifications and creating a new certification.
    
    GET: Returns a list of all certifications with pagination support
    POST: Creates a new certification
    """

    @swagger_auto_schema(
        operation_description="Get list of all certifications",
        manual_parameters=[
            openapi.Parameter(
                'is_active',
                openapi.IN_QUERY,
                description="Filter by is_active status (true/false)",
                type=openapi.TYPE_BOOLEAN
            ),
        ],
        responses={200: CertificationSerializer(many=True)}
    )
    def get(self, request):
        """Retrieve list of certifications with optional filtering"""
        queryset = Certification.objects.all()
        
        # Filter by is_active if provided
        is_active = request.query_params.get('is_active', None)
        if is_active is not None:
            is_active = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active)
        
        serializer = CertificationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new certification",
        request_body=CertificationSerializer,
        responses={201: CertificationSerializer, 400: "Bad Request"}
    )
    def post(self, request):
        """Create a new certification"""
        serializer = CertificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CertificationDetailView(APIView):
    """
    API view for retrieving, updating and deleting a specific certification.
    
    GET: Returns a specific certification by id
    PUT: Updates a specific certification (full update)
    PATCH: Partially updates a specific certification
    DELETE: Deletes a specific certification
    """

    def get_object(self, pk):
        """Helper method to get certification by id"""
        try:
            return Certification.objects.get(pk=pk)
        except Certification.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Get a specific certification by id",
        responses={200: CertificationSerializer, 404: "Not Found"}
    )
    def get(self, request, pk):
        """Retrieve a specific certification"""
        certification = self.get_object(pk)
        if not certification:
            return Response(
                {'error': 'Certification not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CertificationSerializer(certification)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update a specific certification (full update)",
        request_body=CertificationSerializer,
        responses={200: CertificationSerializer, 400: "Bad Request", 404: "Not Found"}
    )
    def put(self, request, pk):
        """Full update a specific certification"""
        certification = self.get_object(pk)
        if not certification:
            return Response(
                {'error': 'Certification not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CertificationSerializer(certification, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update a specific certification",
        request_body=CertificationSerializer,
        responses={200: CertificationSerializer, 400: "Bad Request", 404: "Not Found"}
    )
    def patch(self, request, pk):
        """Partial update a specific certification"""
        certification = self.get_object(pk)
        if not certification:
            return Response(
                {'error': 'Certification not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CertificationSerializer(certification, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a specific certification",
        responses={204: "No Content", 404: "Not Found"}
    )
    def delete(self, request, pk):
        """Delete a specific certification"""
        certification = self.get_object(pk)
        if not certification:
            return Response(
                {'error': 'Certification not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        certification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
