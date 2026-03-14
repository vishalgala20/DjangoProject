# API Testing Guide

This guide provides practical examples for testing the Django REST Framework API using cURL commands.

## Prerequisites

- Running Django development server: `python manage.py runserver`
- API available at: `http://localhost:8000/api/`
- Swagger UI at: `http://localhost:8000/swagger/`
- ReDoc at: `http://localhost:8000/redoc/`

## Master Entity Operations

### Vendor CRUD

#### Create Vendor
```bash
curl -X POST http://localhost:8000/api/vendors/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Vendor Corp",
    "code": "NVC001",
    "description": "A new vendor company",
    "is_active": true
  }'
```

#### List Vendors
```bash
curl http://localhost:8000/api/vendors/
```

#### List Active Vendors Only
```bash
curl "http://localhost:8000/api/vendors/?is_active=true"
```

#### Get Specific Vendor
```bash
curl http://localhost:8000/api/vendors/1/
```

#### Fully Update Vendor
```bash
curl -X PUT http://localhost:8000/api/vendors/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Vendor Name",
    "code": "UPDV001",
    "description": "Updated description",
    "is_active": true
  }'
```

#### Partially Update Vendor
```bash
curl -X PATCH http://localhost:8000/api/vendors/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Partially Updated Name"
  }'
```

#### Delete Vendor
```bash
curl -X DELETE http://localhost:8000/api/vendors/1/
```

---

### Product CRUD

#### Create Product
```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Enterprise Software Suite",
    "code": "ESS001",
    "description": "Complete enterprise solution",
    "is_active": true
  }'
```

#### List Products
```bash
curl http://localhost:8000/api/products/
```

#### Get Product with ID
```bash
curl http://localhost:8000/api/products/1/
```

#### Update Product (PATCH)
```bash
curl -X PATCH http://localhost:8000/api/products/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Updated enterprise solution with new features"
  }'
```

#### Delete Product
```bash
curl -X DELETE http://localhost:8000/api/products/1/
```

---

### Course CRUD

#### Create Course
```bash
curl -X POST http://localhost:8000/api/courses/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Advanced Python Development",
    "code": "PYA201",
    "description": "Master advanced Python concepts",
    "is_active": true
  }'
```

#### List All Courses
```bash
curl http://localhost:8000/api/courses/
```

#### Get Single Course
```bash
curl http://localhost:8000/api/courses/1/
```

---

### Certification CRUD

#### Create Certification
```bash
curl -X POST http://localhost:8000/api/certifications/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Certified Kubernetes Administrator",
    "code": "CKA001",
    "description": "Official Kubernetes certification",
    "is_active": true
  }'
```

#### List All Certifications
```bash
curl http://localhost:8000/api/certifications/
```

---

## Mapping Operations

### Vendor-Product Mapping

#### Create Vendor-Product Mapping
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

#### List All Mappings
```bash
curl http://localhost:8000/api/vendor-product-mappings/
```

#### Filter by Vendor
```bash
curl "http://localhost:8000/api/vendor-product-mappings/?vendor_id=1"
```

#### Filter by Product
```bash
curl "http://localhost:8000/api/vendor-product-mappings/?product_id=1"
```

#### Filter by Primary Mapping
```bash
curl "http://localhost:8000/api/vendor-product-mappings/?primary_mapping=true"
```

#### Combined Filters
```bash
curl "http://localhost:8000/api/vendor-product-mappings/?vendor_id=1&product_id=1&primary_mapping=true"
```

#### Get Single Mapping
```bash
curl http://localhost:8000/api/vendor-product-mappings/1/
```

#### Update Mapping
```bash
curl -X PATCH http://localhost:8000/api/vendor-product-mappings/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "primary_mapping": false
  }'
```

#### Delete Mapping
```bash
curl -X DELETE http://localhost:8000/api/vendor-product-mappings/1/
```

---

### Product-Course Mapping

#### Create Product-Course Mapping
```bash
curl -X POST http://localhost:8000/api/product-course-mappings/ \
  -H "Content-Type: application/json" \
  -d '{
    "product": 1,
    "course": 1,
    "primary_mapping": true,
    "is_active": true
  }'
```

#### List With Filters
```bash
curl "http://localhost:8000/api/product-course-mappings/?product_id=1&course_id=1"
```

#### Get Specific Mapping
```bash
curl http://localhost:8000/api/product-course-mappings/1/
```

---

### Course-Certification Mapping

#### Create Course-Certification Mapping
```bash
curl -X POST http://localhost:8000/api/course-certification-mappings/ \
  -H "Content-Type: application/json" \
  -d '{
    "course": 1,
    "certification": 1,
    "primary_mapping": true,
    "is_active": true
  }'
```

#### List All Mappings
```bash
curl http://localhost:8000/api/course-certification-mappings/
```

#### Filter by Course
```bash
curl "http://localhost:8000/api/course-certification-mappings/?course_id=1"
```

---

## Validation Testing

### Test Duplicate Code Prevention

This should fail (code must be unique):
```bash
# Create first vendor
curl -X POST http://localhost:8000/api/vendors/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Vendor A",
    "code": "VA001",
    "is_active": true
  }'

# Try to create another with same code - should fail
curl -X POST http://localhost:8000/api/vendors/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Vendor B",
    "code": "VA001",
    "is_active": true
  }'
```

Expected Response (400 Bad Request):
```json
{
  "code": ["A vendor with this code already exists."]
}
```

---

### Test Duplicate Mapping Prevention

This should fail (same vendor-product pair cannot exist twice):
```bash
# Create first mapping
curl -X POST http://localhost:8000/api/vendor-product-mappings/ \
  -H "Content-Type: application/json" \
  -d '{
    "vendor": 1,
    "product": 1,
    "primary_mapping": true,
    "is_active": true
  }'

# Try to create same mapping again - should fail
curl -X POST http://localhost:8000/api/vendor-product-mappings/ \
  -H "Content-Type: application/json" \
  -d '{
    "vendor": 1,
    "product": 1,
    "primary_mapping": false,
    "is_active": true
  }'
```

Expected Response (400 Bad Request):
```json
{
  "non_field_errors": ["This vendor-product mapping already exists."]
}
```

---

### Test Primary Mapping Constraint

This should fail (only one primary mapping per parent):
```bash
# Create first primary mapping
curl -X POST http://localhost:8000/api/vendor-product-mappings/ \
  -H "Content-Type: application/json" \
  -d '{
    "vendor": 1,
    "product": 1,
    "primary_mapping": true,
    "is_active": true
  }'

# Try to create another primary mapping for same vendor - should fail
curl -X POST http://localhost:8000/api/vendor-product-mappings/ \
  -H "Content-Type: application/json" \
  -d '{
    "vendor": 1,
    "product": 2,
    "primary_mapping": true,
    "is_active": true
  }'
```

Expected Response (400 Bad Request):
```json
{
  "primary_mapping": ["Only one primary mapping can exist per vendor."]
}
```

---

## Admin Panel Testing

1. Go to `http://localhost:8000/admin/`
2. Login with:
   - Username: `admin`
   - Password: (the password you set when creating superuser)

3. In the admin panel, you can:
   - View all entities and mappings
   - Create/Edit/Delete records
   - Filter by status and date
   - Search by name or code

---

## Python Requests Example

If you prefer to use Python with the requests library:

```python
import requests
import json

API_URL = "http://localhost:8000/api"

# Create vendor
vendor_data = {
    "name": "TechVendor",
    "code": "TV001",
    "description": "A tech vendor",
    "is_active": True
}
response = requests.post(f"{API_URL}/vendors/", json=vendor_data)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

# List vendors
response = requests.get(f"{API_URL}/vendors/")
vendors = response.json()
print(f"Vendors: {vendors}")

# Get specific vendor
response = requests.get(f"{API_URL}/vendors/1/")
vendor = response.json()
print(f"Vendor 1: {vendor}")

# Update vendor
update_data = {"name": "Updated TechVendor"}
response = requests.patch(f"{API_URL}/vendors/1/", json=update_data)
print(f"Updated: {response.json()}")

# Delete vendor
response = requests.delete(f"{API_URL}/vendors/1/")
print(f"Deleted: {response.status_code}")
```

---

## Postman Collection

Import the Swagger JSON into Postman:
1. In Postman, click "Import"
2. Enter URL: `http://localhost:8000/swagger.json`
3. All endpoints will be available for testing

---

## Common Response Codes

- `200 OK` - Successful GET/PUT/PATCH
- `201 Created` - Successful POST
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Validation error
- `404 Not Found` - Resource doesn't exist
- `500 Internal Server Error` - Server error

---

## Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Clear All Data
```bash
python manage.py flush
python manage.py seed_data
```

### View Database Queries
Add to Django settings:
```python
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```
