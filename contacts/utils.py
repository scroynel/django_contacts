import requests
import time
import threading

def fetch_coords_background(city_name):
    # This runs in a separate thread, so it doesn't block the user
    from .models import GeoCache  # Local import to avoid circular imports
    
    if GeoCache.objects.filter(city_name=city_name).exists():
        return

    try:
        # 1. Wait 1.1 seconds to respect Nominatim's limit
        time.sleep(1.1)
        
        headers = {'User-Agent': 'MyWeatherApp/1.0'}
        url = f"https://nominatim.openstreetmap.org/search?q={city_name}&format=json&limit=1"
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data:
                # Use .update() to save to DB without triggering signals
                GeoCache.objects.update_or_create(
                    city_name=city_name,
                    lat=float(data[0]['lat']),
                    lon=float(data[0]['lon'])
                )
    except Exception as e:
        print(f"Background Error: {e}")