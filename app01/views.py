import json
import threading
from datetime import datetime

from django.http import HttpResponse, HttpRequest
from pypinyin import pinyin, Style

from app01.caiyun_weather import city_data, get_city_position_by_name, get_weather_test
# Create your views here.
from app01.models import AirQuality
from app01.spyder import *
from app01.util import simple_post_api, chat


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


@simple_post_api
def air_quality(di):
    if 'city_name' in di and 'date' in di:
        city_name = di['city_name']
        print("air_quality:"+city_name)
        date = di['date'].split("T")[0]
        print("air_quality:"+date)
        data = AirQuality.objects.filter(cityname=city_name, time=date).first()
        response_data = []
        if data:
            response_data = {
                'data': {
                    'time': date,
                    'cityname': city_name,
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
            print(response_data)
        return response_data


def get_city(req: HttpRequest):
    if req.method == "POST":
        return HttpResponse("GET method not supported for this endpoint.")
    elif req.method == "GET":
        # response_data = []
        # city_province_map = {}
        # cities = set()
        # for city_info in city_centers:
        #     city = city_info.get('city')
        #     if city not in cities:
        #         cities.add(city)
        #         province = city_info.get('province')
        #         city_province_map[city] = province
        # count = 0
        # for name in cities:
        #     data = AirQuality.objects.filter(cityname=name, time="2024-05-13").first()
        #     count = count + 1
        #     print(count)
        #     if data:
        #         city_data_entry = {
        #             'data': {
        #                 'time': data.time.strftime('%Y-%m-%d'),
        #                 'cityname': data.cityname,
        #                 'province': city_province_map[data.cityname],
        #                 'aqi': data.aqi,
        #                 'pm2_5': data.pm2_5,
        #                 'pm10': data.pm10,
        #                 'so2': data.so2,
        #                 'no2': data.no2,
        #                 'co': data.co,
        #                 'o3': data.o3,
        #                 'primary_pollutant': data.primary_pollutant
        #             }
        #         }
        #         response_data.append(city_data_entry)
        return HttpResponse(json.dumps(city_data), content_type='application/json')
    else:
        return HttpResponse("Unsupported HTTP method.")


def rank(req: HttpRequest):
    if req.method == "POST":
        return HttpResponse({"ersror": "GET method not supported for this endpoint."})
    elif req.method == "GET":
        city_aqi_map = {}
        city_province_map = {}
        for city_info in city_data:
            data = city_info.get('data')
            city = data.get('cityname')
            aqi = data.get('aqi')
            province = data.get('province')
            city_aqi_map[city] = aqi
            city_province_map[city] = province
            # print(city)
            # print(aqi)
            # print(province)
            # 对城市按照 AQI 值进行排序
        sorted_cities = sorted(city_aqi_map.items(), key=lambda x: x[1], reverse=True)
        response_data = []
        count = 0
        for city, aqi in sorted_cities:
            count = count + 1
            city_data_entry = {
                'cityname': city,
                'province': city_province_map[city],
                'aqi': aqi,
                'rank': count
            }
            response_data.append(city_data_entry)
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        return HttpResponse({"error": "Unsupported HTTP method."})


def annual_weather_func(data):
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
        new_thread.start()

    for t in append_thread_pool:
        try:
            t.join()
        except:
            pass

    res.sort(key=lambda e: e['month'])

    return res


annual_weather = simple_post_api(annual_weather_func)


@simple_post_api
def get_current_weather(data):
    target_city = get_city_position_by_name(data['city'])
    if target_city is not None:
        return get_weather_test(target_city['longitude'], target_city['latitude'])
    else:
        return 404


# 雾霾是近几年来出现频率很高的热门词汇，也是人们关注度最高的热点问题，
# 尤其在人口众多、经济发达的城市，重度空气污染事件频频发生。
# 选择某个或某几个城市分析其空气质量变化情况，
# 探索气温、气压、风向、风速等气象因素、城市建设或人口活动等因素对空气质量的影响

@simple_post_api
def gpt_analysis(data):
    tint_words = "请根据以下json数据，并根据当地人文、地理等因素，分析{}的空气质量变化成因\n\n{}"

    target_city = data['city']

    return {"answer": chat(tint_words.format(target_city, json.dumps(list(map(lambda e: {
        "year": e["year"],
        "month": e['month'],
        "average_temperature": e['average_temperature']['value'],
        "average_aqi": e['average_aqi']['value'],
        "best_air": e['best_air'],
        "worst_air": e['worst_air'],
    }, annual_weather_func({
        "city_pinyin": "".join(map(lambda e: e[0], pinyin(target_city, style=Style.NORMAL))),
        "year": datetime.today().year - 1
    }))))))}
