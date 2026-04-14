import os

import requests
from dotenv import load_dotenv

# .env laden
load_dotenv()

# Token aus Umgebungsvariable holen
ACCESS_TOKEN = os.getenv("MAPBOX_TOKEN")

if not ACCESS_TOKEN:
    raise ValueError("❌ MAPBOX_TOKEN nicht gefunden!")

# Bounding Box (lon1, lat1, lon2, lat2)
lon1, lat1 = 9.1, 47.1
lon2, lat2 = 9.4, 47.3

# Einstellungen
style = "mapbox/streets-v12" # mapbox/dark-v11 mapbox/streets-v12
width = 1280
height = 1280

# URL bauen
url = f"https://api.mapbox.com/styles/v1/{style}/static/[{lon1},{lat1},{lon2},{lat2}]/{width}x{height}@2x?access_token={ACCESS_TOKEN}"

# Request
response = requests.get(url)

if response.status_code == 200:
    os.makedirs("output/maps", exist_ok=True)
    with open("output/maps/map.png", "wb") as f:
        f.write(response.content)
    print("✅ Karte gespeichert als output/maps/map.png")
else:
    print("❌ Fehler:", response.status_code)
    print(response.text)