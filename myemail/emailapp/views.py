from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from emailapp.models import Mail
from django.contrib.auth.models import User

class InForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password"}))

class UpForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Username"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder":"Email"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password"}))

class MessageForm(forms.Form):
    emailfrom = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Your email"}))
    mail = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Write you mail"}))
    emailto = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Where you want send mail"}))
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
    return render(request,'emailapp/userpage.html',{
        "mails":Mail.objects.filter(email_to=request.user.email)|Mail.objects.filter(mail_from=request.user.email)
    })

def login_views(request):
    logout(request)
    return render(request,'emailapp/signin.html',{
        "message":"was logged out",
        "inform":InForm()
    })

def send_message(request):
    if request.method == "GET":
        form = MessageForm(request.GET)
        if form.is_valid():
            mf = form.cleaned_data["emailfrom"]
            m = form.cleaned_data["mail"]
            mt = form.cleaned_data["emailto"]
            newmail = Mail(email_to=mt,mail=m,mail_from=mf)
            newmail.save()
            return HttpResponseRedirect(reverse('emailapp:userpage'))
    return render(request,'emailapp/mmail.html',{
        "mform":MessageForm()
    })