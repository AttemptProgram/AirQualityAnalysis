import re

import requests
from bs4 import BeautifulSoup


def browser(url: str) -> BeautifulSoup:
    soup = BeautifulSoup(
        requests.get(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/97.0.4692.99 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                          '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.9',
                'Connection': 'keep-alive',
            }
        ).text,
        'html.parser'
    )

    for script in soup.find_all('script'):
        script.decompose()

    for style in soup.find_all('style'):
        style.decompose()

    return soup


def get_element_title(tag_element) -> str:
    title = ""
    for i in tag_element.find(class_="tian_twob").stripped_strings:
        title += i
        break
    match title:
        case "平均高温":
            return "average_temperature"
        case "极端高温":
            return "max_temperature"
        case "极端低温":
            return "min_temperature"
        case "平均空气质量指数":
            return "average_aqi"
        case "空气最好":
            return "best_air"
        case "空气最差":
            return "worst_air"
        case _:
            return title


def get_element_value(tag_element):
    meta = tag_element.find(class_="tian_twob").find_all("span")
    return {
        "meta": meta[0].text,
        "value": tag_element.find(class_="tian_twoa").text
    } if len(meta) > 0 and re.match(r"^\s*$", meta[0].text) is None else {
        "value": tag_element.find(class_="tian_twoa").text
    }


def get_city_history_homepage(city_pinyin: str):
    url = f"https://lishi.tianqi.com/{city_pinyin}/index.html"
    print("Target URL:", url)
    soup = browser(url)

    res: dict[str, any] = {
        # "html": soup.prettify()
    }

    res.update({
        get_element_title(tag): get_element_value(tag)
        for tag in soup.find(class_="tian_two").find_all("li")
    })

    res['summarize'] = re.sub(r'\s+', '', soup.find(class_="tianqizongshu_desc").text.split("关注")[0])
    return res


def get_city_history(city_pinyin: str, year: int, month: int):
    url = f"https://lishi.tianqi.com/{city_pinyin}/{str(year).zfill(4) + str(month).zfill(2)}.html"
    print("Target URL:", url)
    soup = browser(url)

    res: dict[str, any] = {
        # "html": soup.prettify()
        "year": year,
        "month": month
    }

    res.update({
        get_element_title(tag): get_element_value(tag)
        for tag in soup.find(class_="tian_two").find_all("li")
    })

    res["daily"] = [
        {
            "date": tag.find_all("div")[0].text.split(" ")[0],
            "data": {
                "max_temperature": tag.find_all("div")[1].text,
                "min_temperature": tag.find_all("div")[2].text,
                "skycon": tag.find_all("div")[3].text,
                "wind": tag.find_all("div")[4].text,
            }
        } for tag in soup.find(class_="thrui").find_all("li")
    ]

    return res


if __name__ == '__main__':
    # with open("output.html", "w") as f:
    #     f.write(browser("https://lishi.tianqi.com/zhongshan/index.html"))
    print(get_city_history_homepage("zhongshan"))
    print(get_city_history("zhongshan", 2023, 10))
