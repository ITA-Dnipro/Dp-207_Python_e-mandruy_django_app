"""django_app URL Configuration
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
from django.contrib import admin
from django.urls import path, include
from user_auth import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('transport/', include('transport.urls')),
    path('home/', views.home_page, name='home'),
    path('user_auth/', include('user_auth.urls')),
    path('hotels/', include('hotels.urls'), name='hotels'),
    path('weather/', include('weather.urls'), name='weather'),
    path('user_profile/', include('user_profile.urls'), name='user_profile'),
    path('subscription/', include('subscription.urls'), name='subscription'),
    path('restaurants/', include('restaurants.urls'), name='restaurants'),
    path('statistics/', include('statistics_app.urls'), name='statistics_app')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
