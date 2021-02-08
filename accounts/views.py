from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import (login as auth_login,  authenticate, logout)
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


def login(request):
    if request.user.is_authenticated:
        messages.error(request,'Please logout first')
        return redirect('receipt_home:print_home')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            raw_password = request.POST['your_pass']
            user = authenticate(username=username, password=raw_password)
            if User.objects.filter(username__iexact=username).exists() is False:
                messages.error(request, 'Username does not exist')
            if user is not None:
                try:
                    auth_login(request, user)
                    messages.success(request, "Logged in")
                    return redirect('receipt_home:print_home')
                except:
                    messages.error(request, 'Something went wrong with the request')
            else:
                messages.error(request, 'something went wrong')
                return render(request, 'login.html', context={})
        if request.method == 'GET':
            return render(request, 'login.html', context={})

def signup(request):
    if request.method == 'POST':
        print(request.user)
        username = request.POST['username']
        raw_password = request.POST['your_pass']
        email_address = '%s@paiyebourhospital.com'%username
        if User.objects.filter(username__iexact=username).exists():
            messages.error(request, "Username is already taken")

        else:
            try:
                user = User.objects.create_user(
                    username, 
                    email_address,
                    raw_password
                )
                user.save()
                user = authenticate(username=username, password=raw_password)
                if user is not None:
                    auth_login(request, user)
                    messages.success(request, "Logged in")
                    # messages.success(request, "Account has been created for %s" %username)
                    return redirect('receipt_home:print_home')
            except:
                messages.error(request, 'Something went wrong with request')
    if request.method == 'GET':
        # print('@@@@@@@@@@@@@@@@@@@@@@@')
        return render(request, 'signup.html')

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out")
        return redirect('accounts:login')
        return render(request, 'cart_home.html')

def view_profile(request):
    return render(request, 'profile.html')
