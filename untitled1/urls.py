"""untitled1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from market.views import *
from market import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('', views.login, name='login'),
    path('seller/', views.main, name='main'),
    #path('seller/product=<int:board_id>', views.view, name='seller_view'),
    path('buyer/', views.main2, name='main2'),
    path('buyer/post=<int:product_id>', views.seller_product, name='buyer_product'),
    path('buyer/wishlist', views.wishlist, name='wishlist'),
    path('seller/write', views.write, name='write_post'),
    path('seller/write/posting', views.posting, name='posting'),
    path('seller/post=<int:product_id>', views.seller_product, name='seller_product'),
    path('seller/post=<int:product_id>/product_delete', views.product_delete, name='product_delete'),
    path('seller/post=<int:product_id>/product_change', views.product_change, name='product_change'),
    path('seller/post=<int:product_id>/product_change/product_changing', views.product_changing,
         name='product_changing'),
]
