from django.urls import path,include
from . import views
app_name = "users"
urlpatterns = [
    path('',views.homepage,name="home"),
    path('register',views.register,name="register"),
    path('logout',views.logout_request,name="logout"),
    path('login',views.login_request,name="login"),
]
