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

def logout(request):
    auth.logout(request)
    return redirect('login')

def main(request):
    user = get_object_or_404(User, username=request.user.username)
    boards = Product.objects.all().filter(seller_name=user.username)
    page = request.GET.get('page', 1)
    paginator = Paginator(boards, 20)
    try:
        lines = paginator.page(page)
    except PageNotAnInteger:
        lines = paginator.page(1)
    except EmptyPage:
        lines = paginator.page(paginator.num_pages)
    context = {'boards': lines}
    return render(request, 'main.html', context)

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
    place = request.POST['place']
    type = request.POST['options']
    phone = request.POST['phone']
    photo = request.FILES['photo']
    content = request.POST['content']
    user = User.objects.get(username=request.user.username)
    user.product_set.create(name=name, price=price, seller_name=user.username, place=place, type=type, photo=photo, phone=phone, status='In Progress', content=content)
    return redirect('main')

#def view(request, board_id):
#    board = Product.objects.get(pk=board_id)
#    board.view += 1
#    board.save()
#    context = {'board': board}
#    return render(request, 'read_post.html', context)

def seller_product(request, product_id) :
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(username=request.user.username)
    product = get_object_or_404(user.product_set, pk=product_id)
    context = {'board' : product}
    return render(request, 'read_post.html', context)

def product_delete(request, product_id) :
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(username=request.user.username)
    product = get_object_or_404(user.product_set, pk=product_id)
    product.delete()

    return redirect('main')


def product_change(request, product_id) :
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(username=request.user.username)
    product = get_object_or_404(user.product_set, pk=product_id)
    context = {'product' : product}
    return render(request, 'change_post.html', context)

def product_changing(request, product_id) :
    if not request.user.is_authenticated:
        return redirect('login')

    user = User.objects.get(username=request.user.username)
    product = user.product_set.get(pk = product_id)

    product.name = request.POST['name']
    product.price = request.POST['price']
    product.place = request.POST['place']
    product.type = request.POST['options']
    product.phone = request.POST['phone']
    product.content = request.POST['content']
    photo = request.FILES.get('photo', False)
    if photo != False :
        product.photo = photo
    product.save()
    return redirect('main')



def wishlist(request) :
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(username=request.user.username)
    boards = user.wish_set.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(boards, 20)
    try:
        lines = paginator.page(page)
    except PageNotAnInteger:
        lines = paginator.page(1)
    except EmptyPage:
        lines = paginator.page(paginator.num_pages)
    context = {'boards': lines}
    return render(request, 'wishlist.html', context)