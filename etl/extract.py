import sys
from pathlib import Path

# add project root to sys.path
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from etl.load import create_table, insert_weather
from datetime import datetime
from pathlib import Path
import os, yaml, requests
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]  # project root
load_dotenv(BASE_DIR / ".env")  # load env vars

# load config
CONFIG_PATH = BASE_DIR / "config" / "config.yaml"
with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

API_KEY_ENV = config["api"].get("api_key_env", "OPENWEATHER_API_KEY")
API_KEY = os.environ.get(API_KEY_ENV)
if not API_KEY:
    raise RuntimeError(
        f"API key not found. Set {API_KEY_ENV} in a .env file or your environment."
    )

CITIES = config.get("cities", [])
if not CITIES:
    print("No cities configured in config/config.yaml. Add at least one city.")
    raise SystemExit(1)

def fetch_weather(city: str) -> dict:
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()

def pretty_print(data: dict):
    name = data.get("name", "N/A")
    temp = data.get("main", {}).get("temp")
    humidity = data.get("main", {}).get("humidity")
    desc = data.get("weather", [{}])[0].get("description")
    print(f"{name}: {temp}°C, humidity={humidity}%, {desc}")

if __name__ == "__main__":
    create_table()
    for city in CITIES:
        try:
            d = fetch_weather(city)
            weather_data = {
                "city": d.get("name", "N/A"),
                "temperature": d.get("main", {}).get("temp"),
                "humidity": d.get("main", {}).get("humidity"),
                "description": d.get("weather", [{}])[0].get("description")
            }
            pretty_print(d)
            insert_weather(weather_data)

        except Exception as e:
            print(f"[ERROR] {city}: {e}")
