from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.homepage,name="home"),
    path('register',views.register,name="register"),
    path('logout',views.logout_request,name="logout"),
    path('login',views.login_request,name="login"),
]
