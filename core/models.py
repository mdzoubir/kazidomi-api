from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)

    # usertype = models.CharField(max_length=20, choices=[
    #     ('admin', 'Admin'),
    #     ('vendor', 'Vendor'),
    #     ('buyer', 'Buyer'),
    # ])
