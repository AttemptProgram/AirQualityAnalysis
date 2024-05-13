import json
from django.core.management.base import BaseCommand
from app01.models import AirQuality
from datetime import datetime, timedelta
from app01.caiyun_weather import city_centers
import pandas as pd


class Command(BaseCommand):
    help = 'Import data into AirQuality model'

    def handle(self, *args, **kwargs):
        self.stdout.write('Importing data...')
        AirQuality.objects.all().delete()

        df = pd.read_csv('aqi_data_u.csv', encoding='utf-8')
        df = df.fillna(0)  # 将 NaN 值替换为 0

        self.stdout.write('DataFrame size: {}'.format(df.shape))

        # 将 DataFrame 转换为字典列表
        data_dicts = df.to_dict(orient='records')

        for row in data_dicts:
            # 将字符串时间转换为日期对象
            time_str = row['time']
            time_date = datetime.strptime(time_str, '%Y-%m-%d')
            # 将日期对象加6年
            new_time_date = time_date + timedelta(days=365 * 6)
            # 将日期对象转换回字符串
            new_time_str = new_time_date.strftime('%Y-%m-%d')
            # 更新字典中的时间字段
            row['time'] = new_time_str

            row['aqi'] = row['aqi'] * 2
        # 批量插入数据
        batch_size = 1000
        for i in range(0, len(data_dicts), batch_size):
            self.stdout.write(str(i))
            AirQuality.objects.bulk_create(
                [AirQuality(**row) for row in data_dicts[i:i + batch_size]]
            )

        response_data = []
        city_province_map = {}
        cities = set()
        for city_info in city_centers:
            city = city_info.get('city')
            if city not in cities:
                cities.add(city)
                province = city_info.get('province')
                city_province_map[city] = province
        count = 0
        for name in cities:
            data = AirQuality.objects.filter(cityname=name, time="2024-05-13").first()
            count = count + 1
            print(count)
            if data:
                city_data_entry = {
                    'data': {
                        'time': data.time,
                        'cityname': data.cityname,
                        'province': city_province_map[data.cityname],
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
                response_data.append(city_data_entry)

        json_data = json.dumps(response_data, indent=4)  # indent 参数用于美化 JSON 文件

        # 将 JSON 字符串写入文件，清空已有内容
        with open('city_data.json', 'w') as json_file:
            json_file.write(json_data)
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
