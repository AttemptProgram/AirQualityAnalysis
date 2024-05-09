from django.core.management.base import BaseCommand
from app01.models import AirQuality
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

        # 批量插入数据
        batch_size = 1000
        for i in range(0, len(data_dicts), batch_size):
            self.stdout.write(str(i))
            AirQuality.objects.bulk_create(
                [AirQuality(**row) for row in data_dicts[i:i+batch_size]]
            )

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
