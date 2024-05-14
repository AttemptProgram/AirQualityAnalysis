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
    # path('api/admin/', admin.site.urls),
    path('api/orm', views.orm),
    path('api/test', views.test),
    path("api/air_quality/", views.air_quality),
    path("api/annually_weather/", views.annual_weather),
    path("api/get_city", views.get_city),
    path("api/get_province", views.get_province),
    path("api/current_weather/", views.get_current_weather),
    path("api/rank", views.rank),
    path("api/gpt_analysis/", views.gpt_analysis),
]
