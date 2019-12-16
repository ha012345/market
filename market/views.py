from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from .models import UserType, Product, UserInfo
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
from django.conf import settings
from datetime import datetime, timedelta, timezone

def signup(request):
    if request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            user = User.objects.create_user(
                username=request.POST["username"], password=request.POST["password1"])
            usertype = request.POST.get("usertype", None)
            type = UserType(user=user, type=usertype)
            type.save()
            userInfo = request.POST.get("student_id", None)
            pw = request.POST.get("password1", None)
            info = UserInfo(user=user, student_id=userInfo, pw=pw)
            info.save()
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
    auctions = Product.objects.all().filter(type = 'auction')
    time2 =  datetime.now(timezone.utc)
    for auction in auctions :
        time1= auction.created_date
        if (time2 -time1).days >= 1 :
            auction.status = 'Bought'
            auction.save()
            history = auction.history_set.all().filter(price = auction.price)
            for histor in history :
                histor.status = 'Bought'
                histor.save()

    user = get_object_or_404(User, username=request.user.username)
    boards = Product.objects.all().filter(seller_name=user.username, status = "In Progress")
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
    auctions = Product.objects.all().filter(type = 'auction')
    time2 =  datetime.now(timezone.utc)
    for auction in auctions :
        time1= auction.created_date
        if (time2 -time1).days >= 1 :
            auction.status = 'Bought'
            auction.save()
            history = auction.history_set.all().filter(price = auction.price)
            for histor in history :
                histor.status = 'Bought'
                histor.save()

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

def main3(request):
    users = User.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(users, 20)
    try:
        lines = paginator.page(page)
    except PageNotAnInteger:
        lines = paginator.page(1)
    except EmptyPage:
        lines = paginator.page(paginator.num_pages)
    context = {'boards': lines}
    return render(request, 'main3.html', context)

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

def buyer_product(request, product_id) :
    if not request.user.is_authenticated:
        return redirect('login')
    product = get_object_or_404(Product, pk=product_id)
    context = {'board' : product}
    return render(request, 'read_post2.html', context)

def buy(request, product_id) :
    print(product_id)
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(username=request.user.username)
    product = Product.objects.get(pk=product_id)
    if not product.history_set.filter(status = 'Bought') :
        if product.type == 'flea' :
            product.history_set.create(user = user, product = product, price = product.price, status='Bought')
            product.status = 'Bought'
            product.save()
        elif product.type == 'auction' :
            product.history_set.create(user = user, product = product, price = request.POST['bid'], status='In Progress')
            product.price = request.POST['bid']
            product.save()

    return redirect('main2')

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

def wish_add(request, product_id) :
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(username=request.user.username)
    product = Product.objects.get(pk = product_id)

    if not user.wish_set.filter(user = user, product=product) :
        user.wish_set.create(user = user, product= product)
    return redirect('buyer_product', product_id)


def wish_erase(request, product_id) :
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(username=request.user.username)
    product = Product.objects.get(pk = product_id)
    wish = get_object_or_404(user.wish_set, product=product)
    wish.delete()
    return redirect('wishlist')


def shoppinglist(request) :
    auctions = Product.objects.all().filter(type = 'auction')
    time2 =  datetime.now(timezone.utc)
    for auction in auctions :
        time1= auction.created_date
        if (time2 -time1).days >= 1 :
            auction.status = 'Bought'
            auction.save()
            history = auction.history_set.all().filter(price = auction.price)
            for histor in history :
                histor.status = 'Bought'
                histor.save()

    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(username=request.user.username)
    boards = user.history_set.filter(status = 'Bought')

    page = request.GET.get('page', 1)
    paginator = Paginator(boards, 20)
    try:
        lines = paginator.page(page)
    except PageNotAnInteger:
        lines = paginator.page(1)
    except EmptyPage:
        lines = paginator.page(paginator.num_pages)
    sum = 0;
    for board in boards :
        sum += board.product.price

    context = {'boards': lines, 'sum' : sum,}
    return render(request, 'shoppinglist.html', context)

def search_product(request):
    all_product = Product.objects.all()
    result = []
    seller_name = request.POST["seller_name"]
    product_name = request.POST["product_name"]
    if request.POST["max"] == '':
        max = 1000000000
    else:
        max = int(request.POST["max"])
    if request.POST["min"] == '':
        min = 0
    else:
        min = int(request.POST["min"])
    for object in all_product.filter(seller_name__contains=seller_name, name__contains=product_name):
        if(min <= object.price <= max):
            result.append(object)
    result.sort(key=lambda object : object.id)
    page = request.GET.get('page', 1)
    paginator = Paginator(result, 8)
    try:
        lines = paginator.page(page)
    except PageNotAnInteger:
        lines = paginator.page(1)
    except EmptyPage:
        lines = paginator.page(paginator.num_pages)
    context = {'boards': lines}
    return render(request, 'main2.html', context)

def member_mod(request, member_id):
    user = User.objects.get(pk=member_id)
    context = {'member' : user}
    return render (request, 'modification.html', context)

def member_mod_1 (request, member_id):
    user = User.objects.get(pk=member_id)
    type = UserType.objects.get(user=user)
    info = UserInfo.objects.get(user=user)
    user.username = request.POST['username']
    user.password = request.POST['pw']
    user.save()
    type.type = request.POST['options']
    type.save()
    info.student_id = request.POST['student_id']
    info.pw = request.POST['pw']
    info.save()
    return redirect('main3')

def member_del(request, member_id):
    user = User.objects.get(pk=member_id)
    type = UserType.objects.get(user=user)
    info = UserInfo.objects.get(user=user)
    info.delete()
    type.delete()
    user.delete()
    return redirect('main3')
