"""Education_Hub_Management_System URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from Education_Hub_Management_System import settings
from MainApp_app import views, AdminViews

urlpatterns = [
    # COMMON
    path('admin/', admin.site.urls),
    path('', views.ShowLoginPage, name='show_login'),
    path('login', views.DoLogin, name='login'),
    path('logout', views.DoLogout, name='logout'),

    # ADMIN
    path('admin_dashboard', AdminViews.Dashboard, name="admin_dashboard"),
    path('admin_profile', AdminViews.Profile, name="admin_profile"),
    path('admin_edit_profile', AdminViews.EditProfile, name="admin_edit_profile"),
    path('admin_edit_profile_save', AdminViews.SaveEditProfile, name="admin_edit_profile_save"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
