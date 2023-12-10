from django.urls import path
from . import views

app_name = "emailapp"

urlpatterns = [
    path("",views.index,name="index"),
    path("signin",views.signin,name="signin"),
    path("signup",views.signup,name="signup"),
    path("userpage",views.userpage,name="userpage"),
    path("logout",views.login_views,name="login_views"),
    path("sendmail",views.send_message,name="mail")
]