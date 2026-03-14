# QUICK START GUIDE

## 🚀 Get Started in 5 Minutes

### Step 1: Setup Environment
```bash
cd c:\Users\Appex\DjangoProject
venv\Scripts\activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run Migrations
```bash
python manage.py makemigrations vendor product course certification vendor_product_mapping product_course_mapping course_certification_mapping
python manage.py migrate
```

### Step 4: Create Admin Account
```bash
python manage.py createsuperuser
# Enter username, email, and password
```

### Step 5: Seed Sample Data
```bash
python manage.py seed_data
```

### Step 6: Start Server
```bash
python manage.py runserver
```

### Step 7: Access the API

**Swagger UI** (Best for testing):
```
http://localhost:8000/swagger/
```

**ReDoc** (Beautiful documentation):
```
http://localhost:8000/redoc/
```

**Admin Panel**:
```
http://localhost:8000/admin/
```

---

## 📝 Basic API Usage

### Create a Vendor
```bash
curl -X POST http://localhost:8000/api/vendors/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Company",
    "code": "MC001",
    "description": "My description",
    "is_active": true
  }'
```

### List Vendors
```bash
curl http://localhost:8000/api/vendors/
```

### Get Specific Vendor
```bash
curl http://localhost:8000/api/vendors/1/
```

### Update Vendor
```bash
curl -X PATCH http://localhost:8000/api/vendors/1/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Name"}'
```

### Delete Vendor
```bash
curl -X DELETE http://localhost:8000/api/vendors/1/
```

---

## 🏗️ Project Structure

```
DjangoProject/
├── manage.py
├── requirements.txt
├── README.md
├── ARCHITECTURE.md
├── API_TESTING_GUIDE.md
├── db.sqlite3
├── config/              ← Main Django project
├── vendor/              ← Master app
├── product/             ← Master app
├── course/              ← Master app
├── certification/       ← Master app
├── vendor_product_mapping/          ← Mapping app
├── product_course_mapping/          ← Mapping app
└── course_certification_mapping/    ← Mapping app
```

---

## 📚 Available Endpoints

### Master Entities
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/vendors/` | List vendors |
| POST | `/api/vendors/` | Create vendor |
| GET | `/api/vendors/<id>/` | Get vendor |
| PUT | `/api/vendors/<id>/` | Update vendor |
| PATCH | `/api/vendors/<id>/` | Partial update |
| DELETE | `/api/vendors/<id>/` | Delete vendor |

Same pattern for `/api/products/`, `/api/courses/`, `/api/certifications/`

### Mappings
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/vendor-product-mappings/` | List mappings |
| POST | `/api/vendor-product-mappings/` | Create mapping |
| GET | `/api/vendor-product-mappings/<id>/` | Get mapping |
| PUT | `/api/vendor-product-mappings/<id>/` | Update mapping |
| PATCH | `/api/vendor-product-mappings/<id>/` | Partial update |
| DELETE | `/api/vendor-product-mappings/<id>/` | Delete mapping |

Same for `/api/product-course-mappings/` and `/api/course-certification-mappings/`

---

## 🔍 Query Parameters

### Filter by Status
```bash
# Get active vendors only
curl "http://localhost:8000/api/vendors/?is_active=true"
```

### Filter Mappings
```bash
# Get mappings for specific vendor
curl "http://localhost:8000/api/vendor-product-mappings/?vendor_id=1"

# Get primary mappings only
curl "http://localhost:8000/api/vendor-product-mappings/?primary_mapping=true"

# Combined filters
curl "http://localhost:8000/api/vendor-product-mappings/?vendor_id=1&primary_mapping=true"
```

---

## ⚙️ Admin Panel Features

1. Go to `http://localhost:8000/admin/`
2. Login with your superuser credentials
3. View/Edit all entities and mappings
4. Search by name or code
5. Filter by status and date
6. Bulk actions available

---

## 🧪 Test the Validations

### Test Duplicate Code (Should Fail)
```bash
# This should fail - code must be unique
curl -X POST http://localhost:8000/api/vendors/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Vendor A",
    "code": "VA001"
  }'

# Try again with same code
curl -X POST http://localhost:8000/api/vendors/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Vendor B",
    "code": "VA001"
  }'
# Response: 400 Bad Request
```

### Test Duplicate Mapping (Should Fail)
```bash
# Create mapping
curl -X POST http://localhost:8000/api/vendor-product-mappings/ \
  -H "Content-Type: application/json" \
  -d '{
    "vendor": 1,
    "product": 1,
    "primary_mapping": true
  }'

# Try to create same mapping again
curl -X POST http://localhost:8000/api/vendor-product-mappings/ \
  -H "Content-Type: application/json" \
  -d '{
    "vendor": 1,
    "product": 1,
    "primary_mapping": false
  }'
# Response: 400 Bad Request
```

### Test Primary Mapping Constraint (Should Fail)
```bash
# Create first primary mapping for vendor 1
curl -X POST http://localhost:8000/api/vendor-product-mappings/ \
  -H "Content-Type: application/json" \
  -d '{
    "vendor": 1,
    "product": 1,
    "primary_mapping": true
  }'

# Try to create another primary mapping for vendor 1
curl -X POST http://localhost:8000/api/vendor-product-mappings/ \
  -H "Content-Type: application/json" \
  -d '{
    "vendor": 1,
    "product": 2,
    "primary_mapping": true
  }'
# Response: 400 Bad Request
```

---

## 🐛 Common Issues & Fixes

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Database Issues
```bash
# Clear database
python manage.py flush

# Recreate
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_data
```

### Import Errors
```bash
# Reinstall everything
pip install -r requirements.txt --force-reinstall
```

### Missing Migrations
```bash
# Create migrations for all apps
python manage.py makemigrations

# Apply them
python manage.py migrate
```

---

## 📖 Documentation Files

- **README.md** - Complete project documentation
- **ARCHITECTURE.md** - In-depth architecture and design patterns
- **API_TESTING_GUIDE.md** - Detailed API testing examples
- **QUICK_START.md** - This file

---

## 🎯 Next Steps

1. **Explore Swagger UI** at `/swagger/` to understand all endpoints
2. **Try creating records** using the cURL examples above
3. **Test validations** to see error messages
4. **Use Admin Panel** to manage records
5. **Review ARCHITECTURE.md** to understand the design
6. **Check API_TESTING_GUIDE.md** for comprehensive examples

---

## 🚀 Deployment Ready

This project includes everything needed for production:
- ✅ Complete API with documentation
- ✅ Validation at model, serializer, and view levels
- ✅ Admin interface
- ✅ Sample data seeding
- ✅ Error handling
- ✅ Audit trail (created_at, updated_at)
- ✅ Soft delete support (is_active)

### For Production:
```bash
# Collect static files
python manage.py collectstatic --noinput

# Use production server (Gunicorn)
gunicorn config.wsgi --bind 0.0.0.0:8000
```

---

## 📞 Support

For detailed information:
- API endpoints → See README.md
- Architecture & design → See ARCHITECTURE.md
- API testing examples → See API_TESTING_GUIDE.md
- Swagger docs → http://localhost:8000/swagger/

---

## ✨ Key Features

✅ **Modular Architecture** - 7 independent apps  
✅ **APIView Based** - No ViewSets, learning-focused  
✅ **Full Documentation** - Swagger/ReDoc  
✅ **Comprehensive Validation** - Model, serializer, view levels  
✅ **Sample Data** - Pre-populated database  
✅ **Admin Interface** - Full CRUD management  
✅ **Error Handling** - User-friendly messages  
✅ **Production Ready** - Settings for deployment  

---

**Server Running?** → http://localhost:8000/swagger/  
**Enjoy building!** 🎉
