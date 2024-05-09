import json

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

# Create your views here.
from app01.models import AirQuality,City



import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def orm(request):
    # 添加
    # AirQuality.objects.create(airQuality=114514,population=114514,size=114514)
    # 删除
    # AirQuality.objects.filter(airQuality=114514).delete()
    # AirQuality.objects.all().delete()
    # 获取
    # data_list = AirQuality.objects.all()
    # print(data_list)
    # for obj in data_list:
    #     print(obj.airQuality, obj.population, obj.size)
    # row_data = data_list.filter(airQuality=1).first #只有一行可以直接.first()
    # print(row_data)
    # 更新
    #AirQuality.objects.all().update(airQuality=123)
    #AirQuality.objects.all().filter(airQuality=114514).update(airQuality=123)
    return HttpResponse("Hello, world. You're at the polls view.")


def test(request):

    return HttpResponse("")


def from_city(req: HttpRequest):
    if req.method == "POST":
        di = json.loads(req.body)
        return HttpResponse(json.dumps({
            "a": "b"
        }))
    elif req.method == "GET":
        pass

    return HttpResponse("Hello World")
