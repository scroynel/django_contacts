import requests
import time

def fetch_coords_background(city_name):
    from .models import GeoCache  # Local import to avoid circular imports
    
    if GeoCache.objects.filter(city_name=city_name).exists():
        return

    try:
        # 1. Wait 1.1 seconds for Nominatim's limit
        time.sleep(1.1)
        
        headers = {'User-Agent': 'MyWeatherApp/1.0'}
        url = f"https://nominatim.openstreetmap.org/search?q={city_name}&format=json&limit=1"
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data:
                GeoCache.objects.update_or_create(
                    city_name=city_name,
                    lat=float(data[0]['lat']),
                    lon=float(data[0]['lon'])
                )
    except Exception as e:
        print(f"Background Error: {e}")


def fetch_weather_by_coords(lats, lons):
    headers = {'User-Agent': 'MyGeocodingApp/1.0'}
                
    weather_api_key = f'https://api.open-meteo.com/v1/forecast?latitude={lats}&longitude={lons}&current_weather=true'

    try:
        response_weather = requests.get(weather_api_key, headers=headers)
        data = response_weather.json()
    except (requests.RequestException, ValueError): # Catch timeout, connection error, http error. ValueError: API -> http, empty response body, jsonDecodeError - invalid json
        data = []

    if isinstance(data, dict):
        data = [data]

    weather = []

    for item in data:
        units = item['current_weather_units']
        values = item['current_weather']
        weather.append({'temp': f'{values['temperature']} {units['temperature']}', 'wind': f'{values['windspeed']} {units['windspeed']}'})

    return weather