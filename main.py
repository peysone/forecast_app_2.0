"""
Zoptymalizuj kod z poprzedniego zadania z pogodą.

Utwórz klasę WeatherForecast, która będzie służyła do odczytywania i zapisywania pliku, a także odpytywania API.

Obiekt klasy WeatherForecast dodatkowo musi poprawnie implementować cztery metody:

 __setitem__
 __getitem__
 __iter__
 items

Wykorzystaj w kodzie poniższe zapytania:

weather_forecast[date] da odpowiedź na temat pogody dla podanej daty
weather_forecast.items() zwróci generator tupli w formacie (data, pogoda)
dla już zapisanych rezultatów przy wywołaniu
weather_forecast to iterator zwracający wszystkie daty, dla których znana jest pogoda
"""


import requests
import json
import os
from datetime import datetime, timedelta


class WeatherForecast:
    def __init__(self):
        self.filename = "forecast_data.json"
        self.data = {}

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                self.data = json.load(file)

    def save_data(self):
        with open(self.filename, "w") as file:
            json.dump(self.data, file)

    def __setitem__(self, date, forecast):
        self.data[date] = forecast
        self.save_data()

    def __getitem__(self, date):
        return self.data.get(date)

    def __iter__(self):
        return iter(self.data)

    def items(self):
        return self.data.items()


def check_rain_forecast(date, latitude, longitude):
    weather_forecast = WeatherForecast()
    weather_forecast.load_data()

    if date is None:
        search_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        search_date = date

    if search_date in weather_forecast:
        return weather_forecast[search_date]

    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon&start_date={search_date}&end_date={search_date}"

    response = requests.get(url)
    response_json = response.json()

    # Sprawdzenie wyniku z API i przypisanie odpowiedniej wartości
    forecast_result = "Nieznana prognoza"
    if "hourly" in response_json and "rain" in response_json["hourly"]:
        rain_values = response_json["hourly"]["rain"]
        if any(rain_values):
            forecast_result = "Bedzie padac"
        else:
            forecast_result = "Nie bedzie padac"

    weather_forecast[search_date] = forecast_result

    return forecast_result



date_to_check = input("Podaj datę w formacie RRRR-mm-dd (np. 2023-06-29): ")
latitude_input = input("Podaj szerokość geograficzną (latitude): ")
longitude_input = input("Podaj długość geograficzną (longitude): ")

forecast_result = check_rain_forecast(date_to_check, latitude_input, longitude_input)
print(f"Prognoza dla {date_to_check}: {forecast_result}")


# Latitude: 54.372158
# Longitude: 18.638306