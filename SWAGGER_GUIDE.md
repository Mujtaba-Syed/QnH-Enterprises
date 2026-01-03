# Swagger/OpenAPI Documentation Guide

This guide explains how to use and access the Swagger API documentation for QnH Enterprises.

## 📚 What is Swagger?

Swagger (OpenAPI) provides interactive API documentation that allows you to:
- View all available API endpoints
- Test API endpoints directly from the browser
- See request/response schemas
- Understand authentication requirements
- Generate client SDKs

## 🚀 Accessing Swagger Documentation

After starting your Django server, you can access the API documentation at:

### Swagger UI (Interactive)
```
http://localhost:8000/api/docs/
```
or in production:
```
https://www.qhenterprises.com/api/docs/
```

### ReDoc (Alternative UI)
```
http://localhost:8000/api/redoc/
```
or in production:
```
https://www.qhenterprises.com/api/redoc/
```

### OpenAPI Schema (JSON/YAML)
```
http://localhost:8000/api/schema/
```
or in production:
```
https://www.qhenterprises.com/api/schema/
```

## 🔐 Authentication in Swagger

The API uses JWT (JSON Web Token) authentication. To test authenticated endpoints:

1. **Get your JWT token** by logging in through the authentication endpoints:
   - `POST /accounts/login/` - Returns access and refresh tokens

2. **Authorize in Swagger UI**:
   - Click the "Authorize" button (🔒) at the top right
   - Enter: `Bearer <your-access-token>`
   - Example: `Bearer eyJ0eXAiOiJKV1QiLCJhbGc...`
   - Click "Authorize"
   - Click "Close"

3. **Now you can test authenticated endpoints** - Swagger will automatically include the token in requests

## 📖 Using Swagger UI

### Viewing Endpoints
- All endpoints are organized by tags (e.g., "Email Testing", "Products", "Cart")
- Click on an endpoint to expand and see details
- Each endpoint shows:
  - HTTP method (GET, POST, PUT, DELETE)
  - Path and parameters
  - Request body schema
  - Response schemas
  - Authentication requirements

### Testing Endpoints

1. **Expand an endpoint** by clicking on it
2. **Click "Try it out"** button
3. **Fill in parameters**:
   - Path parameters (e.g., `product_id`)
   - Query parameters (e.g., `?page=1`)
   - Request body (for POST/PUT requests)
4. **Click "Execute"**
5. **View the response**:
   - Response code (200, 400, 401, etc.)
   - Response body
   - Response headers

### Example: Testing Email Endpoint

1. Navigate to `POST /api/orders/test-email/`
2. Click "Try it out"
3. Enter in the request body:
   ```json
   {
     "email": "test@example.com"
   }
   ```
4. Click "Execute"
5. View the response

## 🛠️ Adding Documentation to Your Views

To add Swagger documentation to your API views, use the `@extend_schema` decorator:

### Basic Example

```python
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response

class MyView(APIView):
    @extend_schema(
        summary="Short description",
        description="Detailed description of what this endpoint does",
        tags=['My Tag'],
        responses={
            200: {
                'description': 'Success response',
                'content': {
                    'application/json': {
                        'example': {'status': 'success', 'data': {}}
                    }
                }
            }
        }
    )
    def get(self, request):
        return Response({'status': 'success'})
```

### With Request Body

```python
@extend_schema(
    summary="Create Order",
    description="Create a new order",
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'product_id': {'type': 'integer'},
                'quantity': {'type': 'integer'},
                'customer_email': {'type': 'string', 'format': 'email'}
            },
            'required': ['product_id', 'quantity']
        }
    },
    responses={
        201: {'description': 'Order created successfully'},
        400: {'description': 'Invalid input'}
    },
    tags=['Orders']
)
def post(self, request):
    # Your view logic
    pass
```

### With Query Parameters

```python
from drf_spectacular.utils import OpenApiParameter

@extend_schema(
    summary="List Products",
    description="Get a list of products with optional filtering",
    parameters=[
        OpenApiParameter(
            name='category',
            type=str,
            location=OpenApiParameter.QUERY,
            description='Filter by category',
            required=False
        ),
        OpenApiParameter(
            name='page',
            type=int,
            location=OpenApiParameter.QUERY,
            description='Page number',
            required=False
        )
    ],
    tags=['Products']
)
def get(self, request):
    # Your view logic
    pass
```

## 📝 Current API Endpoints

The Swagger documentation includes all API endpoints from:

- **Authentication** (`/accounts/`)
  - Register, Login, Logout
  - Password Reset
  - User Profile
  - Google OAuth

- **Products** (`/api/products/`)
  - List products
  - Product details
  - Filter products
  - Featured/New/Best seller products

- **Cart** (`/api/cart/`)
  - View cart
  - Add/Remove items
  - Update quantities
  - Guest cart operations

- **Orders** (`/api/orders/`)
  - Test email endpoints (DEBUG only)

- **Blog** (`/api/blog/`)
  - List blog posts
  - Blog post details

- **Reviews** (`/api/reviews/`)
  - Product reviews

## 🔧 Configuration

Swagger is configured in `core/core/settings.py`:

```python
SPECTACULAR_SETTINGS = {
    'TITLE': 'QnH Enterprises API',
    'DESCRIPTION': 'API documentation for QnH Enterprises e-commerce platform',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': '/api/',
    'AUTHENTICATION_WHITELIST': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': False,
        'filter': True,
        'tagsSorter': 'alpha',
        'operationsSorter': 'alpha',
    },
}
```

## 🎨 Customization

### Change API Title/Description

Edit `SPECTACULAR_SETTINGS` in `settings.py`:

```python
SPECTACULAR_SETTINGS = {
    'TITLE': 'Your Custom API Title',
    'DESCRIPTION': 'Your custom description',
    'VERSION': '2.0.0',
    # ... other settings
}
```

### Add Custom Tags

Tags are automatically generated from view classes, but you can customize:

```python
@extend_schema(tags=['Custom Tag Name'])
def my_view(request):
    pass
```

### Hide Endpoints

To hide an endpoint from Swagger:

```python
from drf_spectacular.utils import extend_schema

@extend_schema(exclude=True)
def hidden_endpoint(request):
    pass
```

## 🐛 Troubleshooting

### Swagger UI not loading
- Check that `drf-spectacular` is installed: `pip install drf-spectacular`
- Verify it's in `INSTALLED_APPS`
- Check Django server logs for errors

### Authentication not working
- Make sure you're using the correct token format: `Bearer <token>`
- Check that the token hasn't expired
- Verify JWT authentication is configured in `REST_FRAMEWORK` settings

### Endpoints not showing
- Ensure views inherit from DRF viewsets or APIView
- Check that views are included in URL patterns
- Verify `DEFAULT_SCHEMA_CLASS` is set in `REST_FRAMEWORK`

### Schema errors
- Check for circular imports in serializers
- Verify all serializers are properly defined
- Review Django server logs for detailed error messages

## 📚 Additional Resources

- [drf-spectacular Documentation](https://drf-spectacular.readthedocs.io/)
- [OpenAPI Specification](https://swagger.io/specification/)
- [Swagger UI Documentation](https://swagger.io/tools/swagger-ui/)

## 🔒 Security Notes

- Swagger endpoints are publicly accessible by default
- In production, consider restricting access to Swagger UI
- Never expose sensitive information in API documentation
- Use proper authentication for all protected endpoints

## 🚀 Next Steps

1. Add `@extend_schema` decorators to all your API views
2. Document request/response schemas
3. Add examples for complex endpoints
4. Organize endpoints with meaningful tags
5. Keep documentation up-to-date as you add new endpoints

