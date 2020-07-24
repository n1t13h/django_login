from django.urls import path,include
from .views import *
urlpatterns = [
    path('',views.homepage,name="home"),
]
