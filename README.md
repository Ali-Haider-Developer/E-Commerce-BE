# E-commerce Backend API

This is the backend API for the E-commerce application built with FastAPI.

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run database migrations:
```bash
alembic upgrade head
```

5. Start the server:
```bash
uvicorn app.main:app --reload
```

## API Documentation

### Authentication

#### Admin Authentication
- `POST /auth/signup`
  - Create new admin user
  - Body: `{"email": "admin@example.com", "password": "password", "full_name": "Admin User"}`
  - Response: `{"access_token": "token", "token_type": "bearer"}`

- `POST /auth/login`
  - Login as admin
  - Body: `{"username": "admin@example.com", "password": "password"}`
  - Response: `{"access_token": "token", "token_type": "bearer"}`

#### User Authentication
- `POST /auth/register`
  - Register new user
  - Body: `{"email": "user@example.com", "password": "password", "full_name": "User Name"}`
  - Response: User details

- `POST /auth/login`
  - Login as user
  - Body: `{"username": "user@example.com", "password": "password"}`
  - Response: `{"access_token": "token", "token_type": "bearer"}`

### Admin Endpoints

#### Users Management
- `GET /users/`
  - List all users (admin only)
  - Query params: skip, limit
  - Response: List of users

- `GET /users/{user_id}`
  - Get user details (admin only)
  - Response: User details

- `POST /users/`
  - Create new user (admin only)
  - Body: UserCreate schema
  - Response: Created user

- `PUT /users/{user_id}`
  - Update user (admin only)
  - Body: UserUpdate schema
  - Response: Updated user

- `DELETE /users/{user_id}`
  - Delete user (admin only)
  - Response: Success message

#### Categories Management
- `GET /categories/`
  - List all categories (admin only)
  - Response: List of categories

- `POST /categories/`
  - Create new category (admin only)
  - Body: CategoryCreate schema
  - Response: Created category

- `PUT /categories/{category_id}`
  - Update category (admin only)
  - Body: CategoryUpdate schema
  - Response: Updated category

- `DELETE /categories/{category_id}`
  - Delete category (admin only)
  - Response: Success message

#### Products Management
- `GET /products/`
  - List all products (admin only)
  - Query params: skip, limit, category_id
  - Response: List of products

- `POST /products/`
  - Create new product (admin only)
  - Body: ProductCreate schema
  - Response: Created product

- `PUT /products/{product_id}`
  - Update product (admin only)
  - Body: ProductUpdate schema
  - Response: Updated product

- `DELETE /products/{product_id}`
  - Delete product (admin only)
  - Response: Success message

#### Product Variants Management
- `POST /products/{product_id}/variants`
  - Create product variant (admin only)
  - Body: ProductVariantCreate schema
  - Response: Created variant

- `PUT /products/{product_id}/variants/{variant_id}`
  - Update product variant (admin only)
  - Body: ProductVariantUpdate schema
  - Response: Updated variant

- `DELETE /products/{product_id}/variants/{variant_id}`
  - Delete product variant (admin only)
  - Response: Success message

#### Orders Management
- `GET /orders/`
  - List all orders (admin only)
  - Query params: skip, limit, status
  - Response: List of orders

- `GET /orders/{order_id}`
  - Get order details (admin only)
  - Response: Order details

- `PUT /orders/{order_id}/status`
  - Update order status (admin only)
  - Body: OrderStatusUpdate schema
  - Response: Updated order

#### Settings Management
- `GET /settings/admin`
  - List all settings (admin only)
  - Response: List of settings

- `POST /settings/admin`
  - Create new setting (admin only)
  - Body: SettingsCreate schema
  - Response: Created setting

- `PUT /settings/admin/{setting_id}`
  - Update setting (admin only)
  - Body: SettingsUpdate schema
  - Response: Updated setting

- `DELETE /settings/admin/{setting_id}`
  - Delete setting (admin only)
  - Response: Success message

### User Endpoints

#### Products
- `GET /products/`
  - List all products
  - Query params: skip, limit, category_id, search
  - Response: List of products

- `GET /products/{product_id}`
  - Get product details
  - Response: Product details

- `GET /products/{product_id}/variants`
  - Get product variants
  - Response: List of variants

#### Categories
- `GET /categories/`
  - List all categories
  - Response: List of categories

#### Cart Operations
- `GET /cart/`
  - Get user's cart
  - Response: Cart details

- `POST /cart/items`
  - Add item to cart
  - Body: CartItemCreate schema
  - Response: Updated cart

- `PUT /cart/items/{item_id}`
  - Update cart item
  - Body: CartItemUpdate schema
  - Response: Updated cart

- `DELETE /cart/items/{item_id}`
  - Remove item from cart
  - Response: Updated cart

- `DELETE /cart/`
  - Clear cart
  - Response: Empty cart

#### Wishlist Operations
- `GET /wishlist/`
  - Get user's wishlist
  - Response: Wishlist details

- `POST /wishlist/items`
  - Add item to wishlist
  - Body: WishlistItemCreate schema
  - Response: Updated wishlist

- `DELETE /wishlist/items/{item_id}`
  - Remove item from wishlist
  - Response: Updated wishlist

- `DELETE /wishlist/`
  - Clear wishlist
  - Response: Empty wishlist

#### Orders
- `POST /orders/`
  - Create new order
  - Body: OrderCreate schema
  - Response: Created order

- `GET /orders/`
  - List user's orders
  - Query params: skip, limit, status
  - Response: List of orders

- `GET /orders/{order_id}`
  - Get order details
  - Response: Order details

#### User Profile
- `GET /users/me`
  - Get current user profile
  - Response: User details

- `PUT /users/me`
  - Update user profile
  - Body: UserUpdate schema
  - Response: Updated user

#### Settings
- `GET /settings/`
  - Get all public settings
  - Response: List of settings

- `GET /settings/{key}`
  - Get specific setting value
  - Response: Setting value

## Authentication

All endpoints except public ones require authentication using JWT tokens. Include the token in the Authorization header:

```
Authorization: Bearer <token>
```

## Error Responses

The API uses standard HTTP status codes:

- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 422: Validation Error
- 500: Internal Server Error

## Data Models

### User
```python
{
    "id": int,
    "email": str,
    "full_name": str,
    "is_active": bool,
    "is_admin": bool,
    "created_at": datetime,
    "updated_at": datetime
}
```

### Product
```python
{
    "id": int,
    "name": str,
    "description": str,
    "category_id": int,
    "price": float,
    "stock": int,
    "images": List[str],
    "attributes": Dict[str, Any],
    "is_active": bool,
    "created_at": datetime,
    "updated_at": datetime,
    "variants": List[ProductVariant]
}
```

### Order
```python
{
    "id": int,
    "user_id": int,
    "shipping_address": Dict[str, Any],
    "payment_method": str,
    "status": OrderStatus,
    "created_at": datetime,
    "updated_at": datetime,
    "items": List[OrderItem]
}
```

### Cart
```python
{
    "id": int,
    "user_id": int,
    "created_at": datetime,
    "updated_at": datetime,
    "items": List[CartItem]
}
```

### Wishlist
```python
{
    "id": int,
    "user_id": int,
    "created_at": datetime,
    "updated_at": datetime,
    "items": List[WishlistItem]
}
```

## Development

### Running Tests
```bash
pytest
```

### Code Style
```bash
black .
isort .
flake8
```

### Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```
