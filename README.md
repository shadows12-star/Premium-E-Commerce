# Premium E-Commerce

A Django-based e-commerce web application built as a practice project. It includes product browsing, category filtering, cart management, customer accounts, order processing, product reviews, product gallery images, email configuration, and SSLCommerz payment integration.
## Screenshots

### Home Page

<img width="1514" height="1155" alt="image" src="https://github.com/user-attachments/assets/4b7e6319-bdbf-4e0c-af32-53d923b045fe" />

### Product Listing Page
<img width="1500" height="953" alt="image" src="https://github.com/user-attachments/assets/001811f0-8942-4a0b-b405-7436d698616f" />


### Product Detail Page
<img width="1583" height="1319" alt="image" src="https://github.com/user-attachments/assets/c5302371-e3c9-4bf0-a5e0-a533f443e0d1" />


### Cart Page
<img width="1680" height="821" alt="image" src="https://github.com/user-attachments/assets/d167387a-371f-4fb7-9cb1-4a7ea1097ec5" />


### Checkout Page
<img width="1718" height="1309" alt="image" src="https://github.com/user-attachments/assets/73a2d851-1686-4e41-839c-eb1e93f7c7e3" />

## Project Overview


**Premium E-Commerce** is a full-stack Django project for learning and practicing core e-commerce features. The project is organized into separate Django apps for accounts, categories, store/product management, cart, and orders.

## Features

### Customer Features

- User registration and login
- Custom user account model
- User profile model with address and profile picture
- Product browsing
- Product detail pages
- Product image gallery
- Product variations such as size and color
- Category-based product navigation
- Search by product name, description, category, and price
- Price filtering
- Size filtering
- Cart system
- Checkout and order placement
- SSLCommerz payment flow
- Order success and payment failure pages
- Product reviews and ratings
- Review restriction so only customers who purchased a product can review it

### Admin / Backend Features

- Django admin panel
- Product management
- Category management
- Product variation management
- Product gallery management
- Order and payment records
- Stock update after successful order
- Email configuration for order confirmation
- Environment variable support using `python-decouple`

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django |
| Database | SQLite |
| Frontend | HTML, CSS, Bootstrap |
| Forms | Django Forms, Crispy Forms, Crispy Bootstrap 5 |
| Authentication | Custom Django user model |
| Payments | SSLCommerz |
| Static & Media | Django static files and media upload |
| Email | SMTP / Gmail configuration |

## Project Structure

```text
Premium-E-Commerce/
│
├── accounts/          # Custom user account and profile
├── cart/              # Cart and cart item logic
├── categories/        # Product categories
├── ecommerce/         # Main Django project settings and URLs
├── orders/            # Order, payment, and checkout logic
├── static/            # Static assets
├── store/             # Products, variations, reviews, gallery
├── templates/         # HTML templates
├── manage.py
└── .gitignore
```

## Main Apps

### `accounts`

Handles user registration, authentication, custom account model, and user profile information.

### `categories`

Handles product categories and category-based navigation.

### `store`

Handles product listing, product details, product variations, product gallery, product reviews, searching, filtering, pagination, and product ratings.

### `cart`

Handles shopping cart items, quantities, selected product variations, and subtotal calculation.

### `orders`

Handles checkout, order creation, payment records, SSLCommerz payment validation, order products, stock reduction, and order confirmation email.

## Environment Variables

Create a `.env` file in the project root, beside `manage.py`.

```env
SECRET_KEY=your_django_secret_key

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_gmail_app_password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=your_email@gmail.com

SSL_COMMERZ_STORE_ID=your_sslcommerz_store_id
SSL_COMMERZ_STORE_PASSWORD=your_sslcommerz_store_password
SSL_COMMERTZ_PAYMENT_URL=https://sandbox.sslcommerz.com/gwprocess/v4/api.php
SSL_COMMERZ_VALIDATION_URL=https://sandbox.sslcommerz.com/validator/api/validationserverAPI.php
```

> Never upload your `.env` file to GitHub.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/shadows12-star/Premium-E-Commerce.git
cd Premium-E-Commerce
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**macOS / Linux**

```bash
source venv/bin/activate
```

### 3. Install dependencies

If you already have a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

If not, install the main packages manually:

```bash
pip install django python-decouple django-crispy-forms crispy-bootstrap5 requests pillow
```

### 4. Create `.env`

Create a `.env` file and add the required environment variables listed above.

### 5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

Open the project in your browser:

```text
http://127.0.0.1:8000/
```

## Media and Static Files

The project uses media uploads for product images, product gallery images, and profile pictures.

Development media settings should include:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

Development static settings should include:

```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

In the main `urls.py`, media files should be served during development using:

```python
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## Payment Flow

The project uses SSLCommerz sandbox payment flow:

1. User places an order.
2. System creates an order number.
3. User is redirected to SSLCommerz payment gateway.
4. SSLCommerz sends success or failure response.
5. On successful validation:
   - Payment record is created.
   - Order is marked as ordered.
   - Ordered products are saved.
   - Product stock is reduced.
   - Cart items are cleared.
   - Confirmation email is sent.

## Review System

Customers can submit product reviews only after purchasing the product. The system checks whether the user has an ordered `OrderProduct` for that product before allowing a review.

## Useful Commands

```bash
python manage.py runserver
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

## Security Notes

- Keep `SECRET_KEY`, email password, and SSLCommerz credentials inside `.env`.
- Do not commit `.env` to GitHub.
- Use Gmail App Password instead of your real Gmail password.
- Set `DEBUG = False` in production.
- Add real domain names to `ALLOWED_HOSTS` in production.
- Use proper production hosting for media and static files.

## Future Improvements

- Add wishlist functionality
- Add coupon or discount system
- Add order tracking dashboard
- Add product stock alerts
- Add product recommendation system
- Improve payment error handling
- Add API endpoints using Django REST Framework
- Add deployment configuration

## Author

**shadows12-star**

GitHub: `https://github.com/shadows12-star`

## License

This project is for practice and learning purposes. Add a license file if you plan to make it open-source.
