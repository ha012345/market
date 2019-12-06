from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import UserType, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
from django.conf import settings

def main(request):
    return render(request, 'main.html')

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