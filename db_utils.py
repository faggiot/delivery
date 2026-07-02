import sqlite3

DB_PATH = "delivery.db"

def get_all_cities():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT name FROM cities ORDER BY name")
    cities = [row[0] for row in cur.fetchall()]
    conn.close()
    return cities

def get_distance(city1, city2):
    if city1 == city2:
        return 0
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT km FROM distances WHERE city1=? AND city2=?", (city1, city2))
    result = cur.fetchone()
    conn.close()
    return result[0] if result else 100

def get_carriers(include_express=False):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    query = "SELECT name, base_cost, cost_per_kg, cost_per_km, speed FROM carriers"
    if not include_express:
        query += " WHERE is_express = 0"
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    return rows