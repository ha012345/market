from django.contrib import admin
from .models import UserType, Product, History, Wish

admin.site.register(UserType)
admin.site.register(Product)
admin.site.register(History)
admin.site.register(Wish)
