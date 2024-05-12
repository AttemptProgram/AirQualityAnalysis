import json

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
# Create your views here.
from app01.models import AirQuality
from app01.caiyun_weather import city_data, get_city_position_by_name, get_weather
from app01.spyder import *

from app01.util import simple_post_api


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
    # AirQuality.objects.all().update(airQuality=123)
    # AirQuality.objects.all().filter(airQuality=114514).update(airQuality=123)
    return HttpResponse("Hello, world. You're at the polls view.")


def test(request):
    return HttpResponse("{\"message\": \"Hello World\"}")


def air_quality(req: HttpRequest):
    if req.method == "POST":
        di = json.loads(req.body)
        if 'city_name' in di and 'date' in di:
            city_name = di['city_name']
            date = di['date']
            data = AirQuality.objects.filter(cityname=city_name, time=date).first()
            response_data = []
            if data:
                response_data = {
                    'data': {
                        'time': data.time.strftime('%Y-%m-%d'),
                        'cityname': data.cityname,
                        'aqi': data.aqi,
                        'pm2_5': data.pm2_5,
                        'pm10': data.pm10,
                        'so2': data.so2,
                        'no2': data.no2,
                        'co': data.co,
                        'o3': data.o3,
                        'primary_pollutant': data.primary_pollutant
                    }
                }
            return HttpResponse(json.dumps(response_data), content_type='application/json')
    elif req.method == "GET":
        return HttpResponse("GET method not supported for this endpoint.")
    else:
        return HttpResponse("Unsupported HTTP method.")


def get_city(req: HttpRequest):
    if req.method == "POST":
        return HttpResponse("GET method not supported for this endpoint.")
    elif req.method == "GET":
        #     response_data = []
        #     city_province_map = {}
        #     cities = set()
        #     for city_info in city_data:
        #         city = city_info.get('city')
        #         if city not in cities:
        #             cities.add(city)
        #             province = city_info.get('province')
        #             city_province_map[city] = province
        #     print(cities)
        #     count=0
        #     for name in cities:
        #         data = AirQuality.objects.filter(cityname=name, time="2024-05-13").first()
        #         count=count+1
        #         print(count)
        #         if data:
        #             city_data_entry = {
        #                 'data': {
        #                     'time': data.time.strftime('%Y-%m-%d'),
        #                     'cityname': data.cityname,
        #                     'aqi': data.aqi,
        #                     'pm2_5': data.pm2_5,
        #                     'pm10': data.pm10,
        #                     'so2': data.so2,
        #                     'no2': data.no2,
        #                     'co': data.co,
        #                     'o3': data.o3,
        #                     'primary_pollutant': data.primary_pollutant
        #                 }
        #             }
        #             response_data.append(city_data_entry)
        return HttpResponse(json.dumps(city_data), content_type='application/json')
    else:
        return HttpResponse("Unsupported HTTP method.")


def rank(req):
    if req.method == "POST":
        return HttpResponse({"error": "GET method not supported for this endpoint."})
    elif req.method == "GET":
        city_aqi_map = {}
        for city_info in city_data:
            city = city_info.get('cityname')
            aqi = city_info.get('aqi')
            city_aqi_map[city] = aqi

            # 对城市按照 AQI 值进行排序
        sorted_cities = sorted(city_aqi_map.items(), key=lambda x: x[1])

        # 构建排序后的城市列表
        sorted_city_list = [{"city": city, "aqi": aqi} for city, aqi in sorted_cities]

        return HttpResponse(sorted_city_list, safe=False)
    else:
        return HttpResponse({"error": "Unsupported HTTP method."})


@simple_post_api
def annual_weather(data):
    city = data['city_pinyin']
    year = data['year']
    res = []
    append_thread_pool = []

    def append_res(index: int):
        try:
            res.append(get_city_history(city, year, index))
        except:
            pass

    for i in range(1, 13):
        new_thread = threading.Thread(target=lambda: append_res(i))
        append_thread_pool.append(new_thread)
        new_thread.run()

    for t in append_thread_pool:
        try:
            t.join()
        except:
            pass

    res.sort(key=lambda e: e['month'])

    return res


@simple_post_api
def get_current_weather(data):
    target_city = get_city_position_by_name(data['city'])
    if target_city is not None:
        return get_weather(target_city['longitude'], target_city['latitude'])
    else:
        return 404
