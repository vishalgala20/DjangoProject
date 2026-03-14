# PROJECT ARCHITECTURE & IMPLEMENTATION DETAILS

## Overview

This is a modular Django REST Framework API system using **APIView only** (no ViewSets) with complete API documentation through drf-yasg. The project demonstrates proper DRF fundamentals by implementing all HTTP methods manually.

## Architecture Decisions

### 1. App Modularity

**Why separate apps?**
- Each entity is isolated and independently deployable
- Clear separation of concerns
- Easy to test individual modules
- Follows Django best practices
- Scalable for team development

**Master Apps:**
- `vendor` - Vendor entity management
- `product` - Product entity management
- `course` - Course entity management
- `certification` - Certification entity management

**Mapping Apps:**
- `vendor_product_mapping` - Vendor ↔ Product relationships
- `product_course_mapping` - Product ↔ Course relationships
- `course_certification_mapping` - Course ↔ Certification relationships

### 2. APIView Implementation

**Why APIView and not ViewSets?**
- Demonstrates understanding of DRF fundamentals
- Explicit control over HTTP methods
- Better understanding of request/response flow
- Custom error handling per method
- More transparent code for interviews

**Structure per API:**
```python
class EntityListCreateView(APIView):
    def get(self, request):      # List entities
        ...
    def post(self, request):     # Create entity
        ...

class EntityDetailView(APIView):
    def get(self, request, pk):  # Retrieve entity
        ...
    def put(self, request, pk):  # Full update
        ...
    def patch(self, request, pk):  # Partial update
        ...
    def delete(self, request, pk):  # Delete entity
        ...
```

### 3. Model Design Patterns

#### Master Entity Model Pattern
```python
class Entity(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100, unique=True)  # Unique identifier
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)        # Soft delete support
    created_at = models.DateTimeField(auto_now_add=True) # Audit trail
    updated_at = models.DateTimeField(auto_now=True)     # Audit trail
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.code})"
```

#### Mapping Model Pattern
```python
class Mapping(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    primary_mapping = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['parent', 'child']  # Prevent duplicates
        ordering = ['-created_at']
    
    def clean(self):
        # Custom validation logic
        pass
    
    def __str__(self):
        return f"{self.parent} -> {self.child}"
```

### 4. Validation Strategy

**Three-layer validation:**

1. **Model Level** (`models.py`)
   - Primary key uniqueness
   - Foreign key relationships
   - `clean()` method for business logic
   - Unique together constraints

2. **Serializer Level** (`serializers.py`)
   - Field-level validation (required, type, length)
   - Cross-field validation
   - Custom validators
   - Business rule enforcement

3. **View Level** (`views.py`)
   - HTTP method validation
   - Authorization/permissions (if needed)
   - Response formatting
   - Error handling

**Validation Implementation:**
```python
# In Serializer
def validate_code(self, value):
    """Field-level validation"""
    if Entity.objects.filter(code=value).exists():
        raise serializers.ValidationError("Code must be unique")
    return value

def validate(self, data):
    """Cross-field validation"""
    if data.get('primary_mapping'):
        # Check business rule
        if OtherMapping.objects.filter(parent=data['parent'], 
                                       primary_mapping=True).exists():
            raise serializers.ValidationError("Only one primary mapping allowed")
    return data
```

### 5. Error Handling Pattern

```python
def get_object(self, pk):
    """Consistent pattern for retrieving objects"""
    try:
        return Entity.objects.get(pk=pk)
    except Entity.DoesNotExist:
        return None

def get(self, request, pk):
    entity = self.get_object(pk)
    if not entity:
        return Response(
            {'error': 'Entity not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = EntitySerializer(entity)
    return Response(serializer.data, status=status.HTTP_200_OK)
```

### 6. Filtering Implementation

```python
def get(self, request):
    queryset = Entity.objects.all()
    
    # Method-specific filter support
    is_active = request.query_params.get('is_active', None)
    if is_active is not None:
        is_active = is_active.lower() == 'true'
        queryset = queryset.filter(is_active=is_active)
    
    serializer = EntitySerializer(queryset, many=True)
    return Response(serializer.data)
```

### 7. Swagger/drf-yasg Documentation

```python
@swagger_auto_schema(
    operation_description="Get list of all entities",
    manual_parameters=[
        openapi.Parameter(
            'is_active',
            openapi.IN_QUERY,
            description="Filter by active status",
            type=openapi.TYPE_BOOLEAN
        ),
    ],
    responses={200: EntitySerializer(many=True)}
)
def get(self, request):
    """Retrieve entities with filtering"""
    ...
```

**Documentation includes:**
- Operation descriptions
- Query parameter documentation
- Request body schemas
- Response schemas
- HTTP status codes
- Error response examples

## Data Flow

### Create Flow
```
Client Request
    ↓
View Layer (APIView.post)
Validates HTTP method
    ↓
Serializer Validation
- Field validation
- Cross-field validation
- Business rule checks
    ↓
Model Validation
- clean() method
- Unique constraints
- Foreign key validation
    ↓
Database Insert
    ↓
Serializer Serialization
Convert model instance to JSON
    ↓
Response (201 Created)
```

### Update Flow
```
Client Request (PUT/PATCH)
    ↓
Retrieve Object
Get from database
    ↓
Serializer Validation
partial=True for PATCH
partial=False for PUT
    ↓
Model Validation
clean() method
    ↓
Database Update
    ↓
Serializer Serialization
    ↓
Response (200 OK)
```

### Delete Flow
```
Client Request (DELETE)
    ↓
Retrieve Object
    ↓
Check if exists
    ↓
Delete from database
    ↓
Response (204 No Content)
```

## Key Features

### 1. Soft Delete Support
Using `is_active` field for soft deletion:
```python
# Instead of DELETE
vendor.is_active = False
vendor.save()

# Query active records
Vendor.objects.filter(is_active=True)
```

### 2. Audit Trail
Automatic timestamps on all entities:
```python
created_at = models.DateTimeField(auto_now_add=True)  # Set once
updated_at = models.DateTimeField(auto_now=True)      # Auto-updated
```

### 3. Primary Mapping Constraint
Only one primary mapping per parent:
```python
# Validation in model and serializer
if primary_mapping:
    existing = Mapping.objects.filter(
        parent=self.parent,
        primary_mapping=True
    ).exclude(id=self.id)
    if existing.exists():
        raise ValidationError("Only one primary mapping allowed")
```

### 4. Relationship Integrity
Foreign key constraints prevent orphaned records:
```python
vendor = models.ForeignKey(
    Vendor,
    on_delete=models.CASCADE,  # Delete mapping if vendor deleted
    related_name='product_mappings'  # Reverse relation
)
```

## Code Quality Standards

### Naming Conventions
- `Models`: Singular, CamelCase (`Vendor`, `Product`)
- `Views`: Descriptive with suffix (`VendorListCreateView`)
- `Serializers`: Model name + "Serializer" (`VendorSerializer`)
- `URLs`: Plural, kebab-case (`/api/vendors/`)
- `Methods`: Lowercase, descriptive (`get_object`, `validate_code`)

### Documentation Standards
```python
class VendorListCreateView(APIView):
    """
    API view for listing all vendors and creating a new vendor.
    
    GET: Returns a list of all vendors with pagination support
    POST: Creates a new vendor
    """

    def get(self, request):
        """Retrieve list of vendors with optional filtering"""
        ...
```

### Error Messages
- User-friendly and specific
- Actionable feedback
- Consistent format

```python
raise serializers.ValidationError(
    "A vendor with this code already exists."
)
```

## Security Considerations

### Current Implementation
- ALLOWED_HOSTS = ['*'] (for development only)
- DEBUG = True (for development only)
- SECRET_KEY in settings (should be in .env)

### Production Recommendations
```python
# settings.py (production)
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECRET_KEY = os.environ.get('SECRET_KEY')

# Add authentication
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# CORS for cross-origin requests
INSTALLED_APPS = [
    ...
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]
```

## Testing Strategy

### Unit Tests
```python
# tests/test_serializers.py
class VendorSerializerTestCase(TestCase):
    def test_valid_serializer(self):
        data = {'name': 'Test', 'code': 'TEST001', 'is_active': True}
        serializer = VendorSerializer(data=data)
        self.assertTrue(serializer.is_valid())
    
    def test_duplicate_code_validation(self):
        Vendor.objects.create(name='V1', code='CODE001')
        data = {'name': 'V2', 'code': 'CODE001'}
        serializer = VendorSerializer(data=data)
        self.assertFalse(serializer.is_valid())
```

### Integration Tests
```python
# tests/test_views.py
class VendorListCreateViewTestCase(TestCase):
    def test_create_vendor(self):
        data = {'name': 'Test', 'code': 'TEST001', 'is_active': True}
        response = self.client.post('/api/vendors/', data)
        self.assertEqual(response.status_code, 201)
    
    def test_list_vendors(self):
        Vendor.objects.create(name='V1', code='CODE001')
        response = self.client.get('/api/vendors/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
```

## Performance Optimizations

### Database Level
```python
# Use select_related for foreign keys
queryset = Mapping.objects.select_related('parent', 'child')

# Use prefetch_related for reverse relations
queryset = Parent.objects.prefetch_related('child_mappings')

# Use only() to fetch specific fields
queryset = Entity.objects.only('id', 'name')
```

### Query Optimization
```python
# Bad: N+1 query problem
for vendor in Vendor.objects.all():
    products = vendor.product_mappings.all()  # Query per vendor

# Good: Use prefetch_related
vendors = Vendor.objects.prefetch_related('product_mappings')
for vendor in vendors:
    products = vendor.product_mappings.all()  # No additional queries
```

### Pagination
```python
# Add to settings
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

# Or limit results in view
if queryset.count() > 1000:
    # Apply pagination
```

## Scalability Considerations

### Horizontal Scaling
- Stateless API design
- Database can be separate
- Use caching for read-heavy operations
- Load balance across multiple servers

### Vertical Scaling
- Database indexing on frequently queried fields
- Connection pooling
- Query optimization
- Caching layer (Redis)

### Example with Caching
```python
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

class VendorListCreateView(APIView):
    @method_decorator(cache_page(60 * 1))  # Cache for 1 minute
    def get(self, request):
        ...
```

## Common Patterns Used

### 1. DRY (Don't Repeat Yourself)
- `get_object()` method reused across detail views
- Consistent serializer validation patterns
- Shared response formatting

### 2. SOLID Principles
- Single Responsibility: One view class per endpoint
- Open/Closed: Easy to extend without modifying
- Template Method Pattern: Request handling in APIView

### 3. Defensive Programming
- Check for None before operations
- Validate foreign keys exist
- Proper exception handling

## Future Enhancements

1. **Authentication & Authorization**
   - Token-based authentication
   - Permission classes
   - User-specific filtering

2. **Advanced Filtering**
   - django-filter integration
   - Date range filtering
   - Full-text search

3. **Caching**
   - Redis integration
   - Query result caching
   - Response caching

4. **Async Support**
   - Async views
   - Background tasks with Celery
   - WebSocket support

5. **Testing**
   - Comprehensive unit tests
   - Integration tests
   - Performance tests

6. **Documentation**
   - OpenAPI 3.0 migration
   - API versioning
   - Changelog

## Dependencies & Versions

```
Django==6.0.3              # Web framework
djangorestframework==3.16.1 # REST API framework
drf-yasg==1.21.15          # API documentation
sqlparse==0.5.5            # SQL formatter
pytz==2026.1.post1         # Timezone support
coreapi==2.3.3             # API schema generation
```

## Deployment Checklist

- [ ] Set DEBUG = False
- [ ] Add SECRET_KEY to environment
- [ ] Update ALLOWED_HOSTS
- [ ] Configure database (PostgreSQL recommended)
- [ ] Set up CORS headers
- [ ] Enable HTTPS
- [ ] Add authentication
- [ ] Set up monitoring
- [ ] Configure logging
- [ ] Add rate limiting
- [ ] Set up backups
- [ ] Configure CDN for static files

## Conclusion

This project demonstrates:
- ✅ Proper Django app modularity
- ✅ DRF APIView fundamentals
- ✅ Comprehensive validation patterns
- ✅ Professional API documentation
- ✅ RESTful best practices
- ✅ Service-oriented architecture
- ✅ Scalable design patterns
