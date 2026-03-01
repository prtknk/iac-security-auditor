import sqlite3
import json
from datetime import datetime

DB_NAME = "scans.db"

def init_db():
    """Creates the SQL table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS scan_reports
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  filename TEXT,
                  timestamp TEXT,
                  vulnerabilities_found INTEGER,
                  details TEXT)''') # We store the complex JSON details as a text string
    conn.commit()
    conn.close()

def save_scan(filename, vulnerabilities):
    """Inserts a new scan report into the database."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO scan_reports (filename, timestamp, vulnerabilities_found, details) VALUES (?, ?, ?, ?)",
              (filename, datetime.now().isoformat(), len(vulnerabilities), json.dumps(vulnerabilities)))
    scan_id = c.lastrowid
    conn.commit()
    conn.close()
    return scan_id