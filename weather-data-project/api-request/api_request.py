# import requests

# api_url = "https://api.weatherstack.com/current?access_key=# api_url = "https://weatherstack.com York"
# =New York"


# def fetch_data():
#     print("Fetching weather data from Weatherstack API...")
#     try:
#         response = requests.get(api_url)
#         response.raise_for_status()
#         print("API response received successfully.")
#         return response.json()
#     except requests.exceptions.RequestExceptions as e:
#         print(f"An error occured:n{e}")
#         raise
    
# fetch_data()

def mock_fetch_data():
    return {'request': {'type': 'City', 'query': 'New York, United States of America', 'language': 'en', 'unit': 'm'}, 'location': {'name': 'New York', 'country': 'United States of America', 'region': 'New York', 'lat': '40.714', 'lon': '-74.006', 'timezone_id': 'America/New_York', 'localtime': '2026-11-12 08:32', 'localtime_epoch': 1794472320, 'utc_offset': '-5.0'}, 'current': {'observation_time': '01:32 PM', 'temperature': 13, 'weather_code': 176, 'weather_icons': ['https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0009_light_rain_showers.png'], 'weather_descriptions': ['Patchy rain nearby'], 'astro': {'sunrise': '06:39 AM', 'sunset': '04:40 PM', 'moonrise': '10:05 AM', 'moonset': '06:48 PM', 'moon_phase': 'Waxing Crescent', 'moon_illumination': 7}, 'air_quality': {'co': '218', 'no2': '52.9', 'o3': '16', 'so2': '2.2', 'pm2_5': '14.3', 'pm10': '16.2', 'us-epa-index': '1', 'gb-defra-index': '1'}, 'wind_speed': 11, 'wind_degree': 91, 'wind_dir': 'E', 'pressure': 1004, 'precip': 0, 'humidity': 73, 'cloudcover': 100, 'feelslike': 11, 'uv_index': 0, 'visibility': 10, 'is_day': 'yes'}}

    