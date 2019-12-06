from django.db import models
from django.contrib.auth.models import User

class UserType (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20);

class Product(models.Model):
    subject = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=30, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True)
    photo = models.ImageField(blank=True)
    view = models.IntegerField(default=0)