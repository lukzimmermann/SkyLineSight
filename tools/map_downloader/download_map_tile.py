import math
import os
from io import BytesIO

import requests
from dotenv import load_dotenv
from PIL import Image

# =========================
# CONFIG
# =========================
load_dotenv()
TOKEN = os.getenv("MAPBOX_TOKEN")

style = "mapbox/streets-v12"

# exakte Bounding Box (lon/lat)
lon_min, lat_min = 9.1, 47.1
lon_max, lat_max = 9.4, 47.3

# gewünschte Auflösung pro Tile (Pixel)
tile_px = 1024

# wie fein schneiden wir die Fläche (mehr = höher Auflösung)
grid_x = 4
grid_y = 4

os.makedirs("output/maps", exist_ok=True)

# =========================
# SIZE OF EACH STEP IN GEO SPACE
# =========================
lon_step = (lon_max - lon_min) / grid_x
lat_step = (lat_max - lat_min) / grid_y

tiles = {}

print("🧭 Generating tiles (bbox-accurate mode)")
print(f"Grid: {grid_x} x {grid_y} = {grid_x * grid_y} tiles")

input("▶️ Press ENTER to start...")

# =========================
# DOWNLOAD
# =========================
for i in range(grid_x):
    for j in range(grid_y):

        lon1 = lon_min + i * lon_step
        lon2 = lon_min + (i + 1) * lon_step

        lat1 = lat_min + j * lat_step
        lat2 = lat_min + (j + 1) * lat_step

        url = (
            f"https://api.mapbox.com/styles/v1/{style}/static/"
            f"[{lon1},{lat1},{lon2},{lat2}]"
            f"/{tile_px}x{tile_px}@2x"
            f"?access_token={TOKEN}"
        )

        print(f"⬇️ Tile {i},{j}")

        r = requests.get(url, timeout=15)

        if r.status_code != 200:
            print("❌ error", r.status_code)
            continue

        img = Image.open(BytesIO(r.content))
        tiles[(i, j)] = img

# =========================
# MERGE
# =========================
final = Image.new("RGB", (grid_x * tile_px * 2, grid_y * tile_px * 2))

for (i, j), img in tiles.items():
    x = i * tile_px * 2
    y = (grid_y - j - 1) * tile_px * 2
    final.paste(img, (x, y))

path = "output/maps/fixed_bbox_highres.png"
final.save(path)

print(f"✅ DONE: {path}")