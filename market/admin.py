from django.contrib import admin
from .models import UserType, Product, History, Wish, UserInfo

admin.site.register(UserType)
admin.site.register(Product)
admin.site.register(History)
admin.site.register(Wish)
admin.site.register(UserInfo)