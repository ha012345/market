from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from .models import UserType, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
from django.conf import settings

def signup(request):
    if request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            user = User.objects.create_user(
                username=request.POST["username"], password=request.POST["password1"])
            usertype = request.POST.get("usertype", None)
            type = UserType(user=user, type=usertype)
            type.save()
            auth.login(request, user)
            if (UserType.objects.get(user=user).type == "seller"):
                return redirect('main')
            else:
                return redirect('main2')
        else:
            return render(request, 'registration/signup.html')
    else:
        return render(request, 'registration/signup.html')

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            if(UserType.objects.get(user=user).type == "seller"):
                return redirect('main')
            else :
                return redirect('main2')
        else:
            return render(request, 'registration/login.html', {'error': 'username or password is incorrect'})
    else:
        return render(request, 'registration/login.html')


def main(request):
    user = get_object_or_404(User, username=request.user.username)
    boards = user.product_set.all()
    return render(request, 'main.html', {'boards' : boards})

def main2(request):
    boards = Product.objects.order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(boards, 20)
    try:
        lines = paginator.page(page)
    except PageNotAnInteger:
        lines = paginator.page(1)
    except EmptyPage:
        lines = paginator.page(paginator.num_pages)
    context = {'boards': lines}
    return render(request, 'main2.html', context)


def write(request) :
    return render(request, 'write_post.html')

def posting(request) :
    if not request.user.is_authenticated:
        return redirect('login')

    name = request.POST['name']
    price = request.POST['price']
    seller_name = request.POST['seller_name']
    place = request.POST['place']
    type = request.POST['options']
    phone = request.POST['phone']
    photo = request.FILES['photo']
    user = User.objects.get(username=request.user.username)
    user.product_set.create(name=name, price=price, seller_name=seller_name, place=place, type=type, photo=photo, phone=phone, status='In Progress')
    return redirect('main')


def seller_product(request, product_id) :
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(username=request.user.username)
    product = get_object_or_404(user.product_set, pk=product_id)
    context = {'product' : product}
    return render(request, 'product_info.html', context)
