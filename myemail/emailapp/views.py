from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.urls import reverse
from emailapp.models import Mail

class InForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password"}))

class UpForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Username"}))
    email = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Email"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password"}))


# Create your views here.
def index(request):
    return render(request,'emailapp/mainpage.html')

def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("emailapp:userpage"))
        else:
            return render(request,'emailapp/signin.html',{
        "inform":InForm(),
        "error":"You are not a User"
        })


    return render(request,'emailapp/signin.html',{
        "inform":InForm()
    })

def signup(request):
    if request.method == "POST":
        form = UpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            if not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists() :
                newuser = User.objects.create_user(username,password=password,email=email)
                newuser.save()
                return HttpResponseRedirect(reverse("emailapp:signin"))
            else:
                return render(request,'emailapp/signup.html',{
                    "upform":UpForm(),
                    "error":"User with same username or email are exist"
                    })

    return render(request,'emailapp/signup.html',{
        "upform":UpForm()
    })

def userpage(request):
    return render(request,'emailapp/userpage.html')

def login_views(request):
    logout(request)
    return render(request,'emailapp/signin.html',{
        "message":"was logged out",
        "inform":InForm()
    })