import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]  # project root
DB_PATH = BASE_DIR / "weather.db"

def create_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS weather(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        temperature REAL,
        humidity REAL,
        description TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def insert_weather(data: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    INSERT INTO weather(city, temperature, humidity, description)
    VALUES (?, ?, ?, ?)
    """, (data["city"], data["temperature"], data["humidity"], data["description"]))
    conn.commit()
    conn.close()
