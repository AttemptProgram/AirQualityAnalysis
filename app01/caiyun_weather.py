from __future__ import annotations

import json
import requests


def get_comprehensive_url(token: str, longitude, latitude):
    return (
        f"https://api.caiyunapp.com/v2.6/TAkhjf8d1nlSlspN/{longitude},{latitude}/weather?"
        f"alert=true&"
        f"dailysteps=3&"
        f"hourlysteps=24&"
        f"token={token}"
    )


def get_weather(lon=120.35, lan=30.31) -> dict | int:
    """
    :return: dict 天气查询结果 , int 天气查询失败后的代码
    """
    response = requests.get(get_comprehensive_url("mkhvpq9w0AsN6gjl", lon, lan))
    if response.status_code == 200:
        resp_data = response.text
        return dict(json.loads(resp_data))
    return response.status_code
