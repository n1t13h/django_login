from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm
from django.utils.http import url_has_allowed_host_and_scheme, is_safe_url
from django.conf import settings
from django.contrib.auth.models import User
# Create your views here.

from django_login.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

import math
import random


def generateOTP():

    # Declare a digits variable
    # which stores all digits
    digits = "0123456789"
    OTP = ""

   # length of password can be chaged
   # by changing value in range
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]

    return OTP


def home_page(request):
    return render(request, "users/index.html", {})


def otp_verify(request):
    if request.method == "POST":
        user = User.objects.get(username=request.POST.get('username'))
        username = request.POST.get('username')
        otp = request.POST.get('otp')
        cotp = request.POST.get('cotp')
        if(otp == cotp):
            user.is_active = True
            user.save()
            messages.success(request, "Account Verified ")
            return redirect("users:homepage")
        else:
            messages.error(request, "Invalid OTP")
            return render(request, 'users/otp.html', {"username": username, "otp": otp})

    return redirect("users:homepage")


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f"New Account Created :{username}")
            # login(request, user)
            subject = 'Email Verification'
            otp = generateOTP()
            message = 'Your OTP is : '+str(otp)
            recepient = str(form.cleaned_data.get('email'))
            print("EMAIL", EMAIL_HOST_USER)
            send_mail(subject, message, EMAIL_HOST_USER,
                      [recepient], fail_silently=False)
            return render(request, 'users/otp.html', {"username": username, "otp": otp})
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}:{form.error_messages[msg]}")

    form = NewUserForm

    return render(request, 'users/register.html', {"form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged Out Successfully")
    return redirect("users:homepage")


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Logged in as:{username}")
                return redirect("users:homepage")
            else:
                messages.error(request, "User Not Found!")

    form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})
