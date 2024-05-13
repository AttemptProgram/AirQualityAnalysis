"""
URL configuration for AirQualityAnalysis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('orm', views.orm),
    path('test', views.test),
    path("air_quality/", views.air_quality),
    path("annually_weather/", views.annual_weather),
    path("get_city", views.get_city),
    path("get_province", views.get_province),
    path("current_weather/", views.get_current_weather),
    path("rank", views.rank),
    path("gpt_analysis/", views.gpt_analysis),
]
