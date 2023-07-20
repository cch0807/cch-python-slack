from dataclasses import dataclass


@dataclass
class WeatherInfo:
    area: str
    now_temperature: str
    lowest_temperature: str
    highest_temperature: str
    status: str
