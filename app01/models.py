import matplotlib
from django.db import models

import pandas as pd


# Create your models here.

# create app01_airquality
# tool 选择 manage.py makemigration migrate
# 新加列时选择1，option 就是默认的值 或者让他允许为空
class AirQuality(models.Model):
    time = models.CharField(max_length=32,default="null",null=True, blank=True)
    cityname = models.CharField(max_length=100, null=True, blank=True)
    aqi = models.FloatField(default=0)
    pm2_5 = models.FloatField(default=0)
    pm10 = models.FloatField(default=0)
    so2 = models.FloatField(default=0)
    no2 = models.FloatField(default=0)
    co = models.FloatField(default=0)
    o3 = models.FloatField(default=0)
    primary_pollutant = models.CharField(default="null",max_length=100, null=True, blank=True)

    # airQuality = models.FloatField(max_length=32)
    # population = models.CharField(max_length=32)
    # size = models.IntegerField()
    # size = models.IntegerField(null = True, blank = True)


class City(models.Model):
    city = models.CharField(max_length=100, null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)



    # AirQuality.objects.create(airQuality=1,population='123',size=114514)

    # df = pd.read_csv('aqi_data_u.csv', encoding='utf-8')
    # df1 = pd.read_csv('city.csv', encoding='gbk')
