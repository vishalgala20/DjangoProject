# Django REST Framework API - Modular Entity & Mapping System

A comprehensive Django REST Framework backend for managing **Vendors**, **Products**, **Courses**, **Certifications** and their relationships using **APIView only** (no ViewSets) with full **drf-yasg** documentation.

## Project Structure

```
DjangoProject/
├── manage.py
├── config/                          # Main project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── vendor/                          # Master app - Vendor
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── apps.py
├── product/                         # Master app - Product
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── apps.py
├── course/                          # Master app - Course
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── apps.py
├── certification/                   # Master app - Certification
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── apps.py
├── vendor_product_mapping/          # Mapping app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── apps.py
├── product_course_mapping/          # Mapping app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── apps.py
├── course_certification_mapping/    # Mapping app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── apps.py
└── requirements.txt
```

## Setup Instructions

### 1. Create and Activate Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
# Follow the prompts to create admin account
```

### 5. Seed Sample Data (Optional)

```bash
python manage.py seed_data
```

### 6. Run Development Server

```bash
python manage.py runserver
```

Server will be running at `http://127.0.0.1:8000/`

## Installed Apps

The project includes the following Django apps configured in `settings.py`:

- **Master Apps**: `vendor`, `product`, `course`, `certification`
- **Mapping Apps**: `vendor_product_mapping`, `product_course_mapping`, `course_certification_mapping`
- **Third-party**: `rest_framework`, `drf_yasg`

## API Documentation & Testing

### Swagger UI (Recommended)
```
http://localhost:8000/swagger/
```

### ReDoc Documentation
```
http://localhost:8000/redoc/
```

### Admin Panel
```
http://localhost:8000/admin/
```

## API Endpoints

### Master Entity APIs

#### Vendor
- `GET /api/vendors/` - List all vendors
- `POST /api/vendors/` - Create a new vendor
- `GET /api/vendors/<id>/` - Retrieve specific vendor
- `PUT /api/vendors/<id>/` - Update vendor (full)
- `PATCH /api/vendors/<id>/` - Partial update vendor
- `DELETE /api/vendors/<id>/` - Delete vendor

#### Product
- `GET /api/products/` - List all products
- `POST /api/products/` - Create a new product
- `GET /api/products/<id>/` - Retrieve specific product
- `PUT /api/products/<id>/` - Update product (full)
- `PATCH /api/products/<id>/` - Partial update product
- `DELETE /api/products/<id>/` - Delete product

#### Course
- `GET /api/courses/` - List all courses
- `POST /api/courses/` - Create a new course
- `GET /api/courses/<id>/` - Retrieve specific course
- `PUT /api/courses/<id>/` - Update course (full)
- `PATCH /api/courses/<id>/` - Partial update course
- `DELETE /api/courses/<id>/` - Delete course

#### Certification
- `GET /api/certifications/` - List all certifications
- `POST /api/certifications/` - Create a new certification
- `GET /api/certifications/<id>/` - Retrieve specific certification
- `PUT /api/certifications/<id>/` - Update certification (full)
- `PATCH /api/certifications/<id>/` - Partial update certification
- `DELETE /api/certifications/<id>/` - Delete certification

### Mapping APIs

#### Vendor-Product Mapping
- `GET /api/vendor-product-mappings/` - List all mappings
- `POST /api/vendor-product-mappings/` - Create mapping
- `GET /api/vendor-product-mappings/<id>/` - Retrieve mapping
- `PUT /api/vendor-product-mappings/<id>/` - Update mapping (full)
- `PATCH /api/vendor-product-mappings/<id>/` - Partial update mapping
- `DELETE /api/vendor-product-mappings/<id>/` - Delete mapping

**Query Parameters:**
- `vendor_id=1` - Filter by vendor
- `product_id=1` - Filter by product
- `primary_mapping=true` - Filter by primary status

#### Product-Course Mapping
- `GET /api/product-course-mappings/` - List all mappings
- `POST /api/product-course-mappings/` - Create mapping
- `GET /api/product-course-mappings/<id>/` - Retrieve mapping
- `PUT /api/product-course-mappings/<id>/` - Update mapping (full)
- `PATCH /api/product-course-mappings/<id>/` - Partial update mapping
- `DELETE /api/product-course-mappings/<id>/` - Delete mapping

**Query Parameters:**
- `product_id=1` - Filter by product
- `course_id=1` - Filter by course
- `primary_mapping=true` - Filter by primary status

#### Course-Certification Mapping
- `GET /api/course-certification-mappings/` - List all mappings
- `POST /api/course-certification-mappings/` - Create mapping
- `GET /api/course-certification-mappings/<id>/` - Retrieve mapping
- `PUT /api/course-certification-mappings/<id>/` - Update mapping (full)
- `PATCH /api/course-certification-mappings/<id>/` - Partial update mapping
- `DELETE /api/course-certification-mappings/<id>/` - Delete mapping

**Query Parameters:**
- `course_id=1` - Filter by course
- `certification_id=1` - Filter by certification
- `primary_mapping=true` - Filter by primary status

## API Usage Examples

### Creating a Vendor

```bash
curl -X POST http://localhost:8000/api/vendors/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "TechCorp",
    "code": "TECH001",
    "description": "Leading technology vendor",
    "is_active": true
  }'
```

### Creating a Product

```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Python Course",
    "code": "PY101",
    "description": "Comprehensive Python programming course",
    "is_active": true
  }'
```

### Creating a Vendor-Product Mapping

```bash
curl -X POST http://localhost:8000/api/vendor-product-mappings/ \
  -H "Content-Type: application/json" \
  -d '{
    "vendor": 1,
    "product": 1,
    "primary_mapping": true,
    "is_active": true
  }'
```

### Listing with Filters

```bash
# Get products by vendor
curl http://localhost:8000/api/vendor-product-mappings/?vendor_id=1

# Get primary mappings only
curl http://localhost:8000/api/vendor-product-mappings/?primary_mapping=true

# Get active vendors only
curl http://localhost:8000/api/vendors/?is_active=true
```

## Model Fields

### Master Entity Models
All master entities (`Vendor`, `Product`, `Course`, `Certification`) include:
- `id` - Auto-generated primary key
- `name` - Entity name (required)
- `code` - Unique code identifier (required)
- `description` - Optional description
- `is_active` - Boolean flag (default: True)
- `created_at` - Timestamp (auto-generated)
- `updated_at` - Timestamp (auto-updated)

### Mapping Models
All mapping models include:
- `id` - Auto-generated primary key
- `<parent>` - Foreign key to parent entity
- `<child>` - Foreign key to child entity
- `primary_mapping` - Boolean flag (default: False)
- `is_active` - Boolean flag (default: True)
- `created_at` - Timestamp (auto-generated)
- `updated_at` - Timestamp (auto-updated)

## Validation Rules

### Master Entity Validations
- **Required Fields**: `name` and `code` are mandatory
- **Unique Code**: Each entity's code must be unique
- **Non-empty Name**: Name cannot be just whitespace

### Mapping Validations
- **Foreign Key Validation**: Parent and child entities must exist
- **Duplicate Prevention**: Same parent-child pair cannot exist twice
  - Example: Cannot create two `Vendor 1 → Product 1` mappings
- **Primary Mapping Constraint**: Only ONE primary mapping per parent
  - If `Vendor 1` has a primary `Product` mapping, attempting to create another primary mapping for `Vendor 1` will fail

## Technical Highlights

### APIView Implementation
- All APIs use DRF's **APIView** class exclusively
- **No ViewSets, GenericAPIView, or mixins** used
- Manual implementation of HTTP methods: `get()`, `post()`, `put()`, `patch()`, `delete()`
- Proper HTTP status codes returned for all operations

### Serializer Validation
- Custom validation for unique codes
- Duplicate mapping prevention at serializer level
- Primary mapping constraint validation
- Required field validation

### Error Handling
- Proper exception handling with meaningful error messages
- Returns 404 when resources not found
- Returns 400 for validation errors
- Returns 204 for successful deletions

### API Documentation
- Every API endpoint documented with `@swagger_auto_schema` decorator
- Request body documentation
- Response schema documentation
- Query parameter documentation
- Success and error response examples

## Database

The project uses **SQLite** by default for development.

### Database File Location
```
db.sqlite3
```

### Making Model Changes
```bash
# Create migration files
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# To reset database (WARNING: deletes all data)
rm db.sqlite3
python manage.py migrate
```

## Admin Interface

Access Django admin at `http://localhost:8000/admin/`

Each app has:
- Complete CRUD interface
- List filters by status and date
- Search functionality
- Read-only timestamps
- Organized fieldsets

## Testing the API

### Using cURL

```bash
# Create vendor
curl -X POST http://localhost:8000/api/vendors/ \
  -H "Content-Type: application/json" \
  -d '{"name": "VendorA", "code": "VA001"}'

# List vendors
curl http://localhost:8000/api/vendors/

# Get single vendor
curl http://localhost:8000/api/vendors/1/

# Update vendor
curl -X PUT http://localhost:8000/api/vendors/1/ \
  -H "Content-Type: application/json" \
  -d '{"name": "UpdatedVendor", "code": "VA001"}'

# Delete vendor
curl -X DELETE http://localhost:8000/api/vendors/1/
```

### Using Postman
1. Open Postman
2. Import the Swagger JSON from `http://localhost:8000/swagger.json`
3. All endpoints will be available in Postman for testing

## Code Quality

- **Modular Structure**: Each app is completely independent
- **DRY Principle**: Consistent patterns across all apps
- **Clear Naming**: Descriptive class and method names
- **Documentation**: Docstrings for all classes and methods
- **Error Messages**: User-friendly error responses

## Dependencies

All dependencies specified in `requirements.txt`:
- **Django 4.2.0** - Web framework
- **djangorestframework 3.14.0** - REST API framework
- **drf-yasg 1.21.6** - API documentation generator
- **sqlparse 0.4.4** - SQL formatter
- **pytz 2024.1** - Timezone support
- **coreapi 2.3.3** - API schema generation

## Common Commands

```bash
# Create superuser
python manage.py createsuperuser

# Run migrations
python manage.py migrate

# Create new app
python manage.py startapp <app_name>

# Open Django shell
python manage.py shell

# Run server with custom host/port
python manage.py runserver 0.0.0.0:8080

# Export data
python manage.py dumpdata > data.json

# Import data
python manage.py loaddata data.json
```

## Troubleshooting

### Port Already in Use
```bash
# Use different port
python manage.py runserver 8001
```

### Database Issues
```bash
# Reset database
python manage.py flush
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Future Enhancements

- [ ] Authentication & Authorization (Token-based)
- [ ] Pagination implementation
- [ ] Advanced filtering with django-filter
- [ ] Unit tests for APIs and serializers
- [ ] Integration tests
- [ ] Soft delete implementation
- [ ] Audit trail logging
- [ ] Rate limiting
- [ ] API versioning
- [ ] GraphQL support

## Support

For issues or questions about the API, refer to:
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [drf-yasg Documentation](https://drf-yasg.readthedocs.io/)

## License

This project is open source and available under the MIT License.
