from django.shortcuts import render , redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import NewUserForm
from django.contrib.auth.models import User
# Create your views here.

def homepage(request):
    return render(request,'users/index.html',{})


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        

        if form.is_valid():
            username=form.cleaned_data.get('username')
            error = User.objects.filter(username='nitishp').count()
            if(error>0):
                messages.error(request,f"Username Already Exist :{username}")
                print("here")
                return redirect("users:register")
            form.save()
            
            messages.success(request,f"New Account Created :{username}")
            login(request,user)
            return redirect("users:home")
        else:
            for msg in form.error_messages:
                messages.error(request,f"{msg}:{form.error_messages[msg]}")


    form = NewUserForm
    
    return render(request,'users/register.html',{"form":form})

def logout_request(request):
    logout(request)
    messages.info(request,"Logged Out Successfully")
    return redirect("users:home")

def login_request(request):
    if request.method=="POST":
        form = AuthenticationForm(request,request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                messages.success(request,f"Logged in as:{username}")
                return redirect("users:home")
            else:
                messages.error(request,"User Not Found!")
        
    form = AuthenticationForm()
    return render(request,"users/login.html",{"form":form})

