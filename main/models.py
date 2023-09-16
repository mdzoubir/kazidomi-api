from uuid import uuid4

from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.


class Promotion(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    users = models.ManyToManyField('Customer', related_name='promotions', blank=True)


class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='category_image')

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1)])
    vendor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    birthday = models.DateField()
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    phone = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username


class Brand(models.Model):
    name = models.CharField(max_length=75)
    description = models.TextField(max_length=255)
    logo = models.ImageField(upload_to='brand_image/')
    cover = models.ImageField(upload_to='brand_image/')
    vendor = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Address(models.Model):
    country = models.CharField(max_length=255)
    zip_code = models.IntegerField()
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="addresses")


class Stock(models.Model):
    quantity = models.PositiveSmallIntegerField()
    stock_date = models.DateField()
    operation = models.CharField(max_length=3, choices=[
        ('in', 'In'),
        ('out', 'Out'),
    ])
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    vendor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        # cart and product value must be unique
        unique_together = [['cart', 'product']]


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    class Meta:
        permissions = [
            ('cancel_order', 'Can cancel order')
        ]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='orderitems')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

    def calculate_total(self):
        return Decimal(self.quantity) * self.unit_price


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
    description = models.TextField()
    created_at = models.DateField(auto_now_add=True)


class ReviewImages(models.Model):
    image = models.ImageField(upload_to='review_image/')
    review = models.ForeignKey(Review, on_delete=models.CASCADE)


class Notification(models.Model):
    message = models.TextField(max_length=450)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Message(models.Model):
    content = models.CharField(max_length=450)
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')


class Payment(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)  # Currency code (e.g., 'USD', 'EUR')
    payment_method = models.CharField(max_length=100)
    payment_source = models.TextField()  # Store payment source details (e.g., Stripe token, PayPal payment details)
    product_id = models.CharField(max_length=100, blank=True, null=True)  # Optional product or service ID
    recipient_info = models.TextField(blank=True, null=True)  # Additional recipient info for bank transfers
    payment_date = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, blank=True,
                                      null=True)  # Store the transaction ID if available
