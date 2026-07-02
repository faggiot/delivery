import sqlite3

def init_database():
    conn = sqlite3.connect("delivery.db")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS distances (
            city1 TEXT NOT NULL,
            city2 TEXT NOT NULL,
            km INTEGER NOT NULL,
            PRIMARY KEY (city1, city2)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS carriers (
            name TEXT PRIMARY KEY,
            base_cost REAL NOT NULL,
            cost_per_kg REAL NOT NULL,
            cost_per_km REAL NOT NULL,
            speed REAL NOT NULL,        -- км/день
            is_express INTEGER DEFAULT 0 -- 1 или 0
        )
    """)

    # === ЗАПОЛНЕНИЕ ДАННЫХ ===
    cities = [
        "Казань", "Набережные Челны", "Альметьевск", "Нижнекамск",
        "Елабуга", "Зеленодольск", "Чистополь", "Бугульма"
    ]
    for c in cities:
        cur.execute("INSERT OR IGNORE INTO cities (name) VALUES (?)", (c,))

    distances = [
        ("Казань", "Набережные Челны", 246), ("Казань", "Альметьевск", 255),
        ("Казань", "Нижнекамск", 204), ("Казань", "Елабуга", 207),
        ("Казань", "Зеленодольск", 43), ("Казань", "Чистополь", 131),
        ("Казань", "Бугульма", 310), ("Набережные Челны", "Альметьевск", 112),
        ("Набережные Челны", "Нижнекамск", 48), ("Набережные Челны", "Елабуга", 35),
        ("Набережные Челны", "Зеленодольск", 289), ("Набережные Челны", "Чистополь", 154),
        ("Набережные Челны", "Бугульма", 173), ("Альметьевск", "Нижнекамск", 112),
        ("Альметьевск", "Елабуга", 126), ("Альметьевск", "Зеленодольск", 310),
        ("Альметьевск", "Чистополь", 150), ("Альметьевск", "Бугульма", 57),
        ("Нижнекамск", "Елабуга", 59), ("Нижнекамск", "Зеленодольск", 290),
        ("Нижнекамск", "Чистополь", 104), ("Нижнекамск", "Бугульма", 165),
        ("Елабуга", "Зеленодольск", 256), ("Елабуга", "Чистополь", 166),
        ("Елабуга", "Бугульма", 190), ("Зеленодольск", "Чистополь", 189),
        ("Зеленодольск", "Бугульма", 370), ("Чистополь", "Бугульма", 187),
    ]
    for c1, c2, km in distances:
        cur.execute("INSERT OR IGNORE INTO distances VALUES (?, ?, ?)", (c1, c2, km))
        cur.execute("INSERT OR IGNORE INTO distances VALUES (?, ?, ?)", (c2, c1, km))

    # Параметры перевозчиков
    carriers = [
        ("Почта России", 120, 30, 0, 80, 0),
        ("СДЭК", 180, 25, 0.8, 150, 0),
        ("СДЭК (экспресс)", 250, 40, 1.2, 300, 1),
        ("ДеливерТат", 100, 20, 0.7, 120, 0),
        ("ЭкспрессDT", 300, 50, 1.5, 999, 1),  # 999 = условно "мгновенно"
    ]
    for c in carriers:
        cur.execute("INSERT OR IGNORE INTO carriers VALUES (?, ?, ?, ?, ?, ?)", c)

    conn.commit()
    conn.close()
    print("База данных delivery.db создана и заполнена")

if __name__ == "__main__":
    init_database()