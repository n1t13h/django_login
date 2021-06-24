from django.urls import path, include
from . import views
app_name = "users"
urlpatterns = [
    path('', views.home_page, name="homepage"),
    path('register', views.register, name="register"),
    path('otp', views.otp_verify, name="otp"),
    path('logout', views.logout_request, name="logout"),
    path('login', views.login_request, name="login"),
]
