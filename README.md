# 空气质量与地理人文因素的关系的分析

> **框架**
> - 后端框架 Django
> - 数据库 MySQL

> **使用技术**
> - BeautifulSoup4 爬虫
> - Requests 对接 WEB 接口

> **外部资源**
> - [天气历史网](https://lishi.tianqi.com)
> - [彩云开放平台](https://platform.caiyunapp.com)
> - [ChatGPT](https://chat.openai.com)

# Django 后端部署指南

> 保证本机或虚拟环境的 Python 版本 >= 3.11.0

## 初始化

```shell
cd path/to/fit/server

git clone https://github.com/AttemptProgram/AirQualityAnalysis.git
cd AirQualityAnalysis

pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py import_data
```

## 运行

```shell
python manage.py runserver 0.0.0.0:8000
```
