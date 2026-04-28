import sqlite3
import os

DB_PATH = "sportguard.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Table for official content fingerprints
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS official_assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            fingerprint TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Table for piracy alerts
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS piracy_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_url TEXT NOT NULL,
            match_percentage REAL,
            status TEXT DEFAULT 'DETECTED',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_fingerprint(filename, fingerprint):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO official_assets (filename, fingerprint) VALUES (?, ?)', (filename, fingerprint))
    conn.commit()
    conn.close()

def get_all_fingerprints():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT fingerprint FROM official_assets')
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]

def log_piracy_alert(url, match_pct):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO piracy_alerts (source_url, match_percentage) VALUES (?, ?)', (url, match_pct))
    conn.commit()
    conn.close()

def get_alerts():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM piracy_alerts ORDER BY timestamp DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows
