"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import path
from assets.views import register

urlpatterns = [
    path('register/', register, name='register'),
    path('registration/login/', auth_views.LoginView.as_view(), name='login'),
    path('', admin.site.urls),  # Arahkan root URL ke Django Admin
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

