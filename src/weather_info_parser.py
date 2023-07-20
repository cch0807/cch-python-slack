import os
import httpx

from dotenv import load_dotenv
from selectolax.parser import HTMLParser
from weather_info import WeatherInfo

load_dotenv()

wheather_url = os.getenv("WHEATHER_URL")


class WeatherInfoParser:
    weatherInfo: WeatherInfo
    html: HTMLParser

    @staticmethod
    def get_today_weather(html) -> WeatherInfo:
        weather_info = WeatherInfo
        weather_info.area = html.css_first("h2.title").text()
        weather_info.now_temperature = html.css_first(
            "div._today div.temperature_text strong"
        ).text(deep=False)
        weather_info.lowest_temperature = (
            html.css("li.today span.lowest")[0].text(deep=False).replace("°", "")
        )
        weather_info.highest_temperature = (
            html.css("li.today span.highest")[0].text(deep=False).replace("°", "")
        )
        weather_info.status = html.css_first(
            "div._today div.weather_graphic div.weather_main span.blind"
        ).text()

        return weather_info

    @staticmethod
    def get_weather(keyword: str) -> HTMLParser:
        try:
            resp = httpx.get(wheather_url + keyword)
            html = HTMLParser(resp.text)
        except Exception as e:
            print("error!!")
            print(e)

        return html
