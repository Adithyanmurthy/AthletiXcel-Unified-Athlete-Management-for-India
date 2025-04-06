import sqlite3
import pandas as pd
import os

DB_PATH = "database.db"
ENHANCED_DB_PATH = "enhanced_features.db"
DATA_FOLDER = "data"

def init_db():
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    # Initialize main database
    conn_main = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor_main = conn_main.cursor()

    # Create users table
    cursor_main.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            name TEXT
        )
    ''')

    # Create athletes table
    cursor_main.execute('''
        CREATE TABLE IF NOT EXISTS athletes (
            username TEXT PRIMARY KEY,
            name TEXT,
            dob TEXT,
            sport TEXT,
            level TEXT,
            FOREIGN KEY(username) REFERENCES users(username)
        )
    ''')

    # Create coaches table
    cursor_main.execute('''
        CREATE TABLE IF NOT EXISTS coaches (
            username TEXT PRIMARY KEY,
            name TEXT,
            specialization TEXT,
            FOREIGN KEY(username) REFERENCES users(username)
        )
    ''')

    # Create coach_assignments table
    cursor_main.execute('''
        CREATE TABLE IF NOT EXISTS coach_assignments (
            coach TEXT,
            athlete TEXT,
            PRIMARY KEY (coach, athlete),
            FOREIGN KEY(coach) REFERENCES users(username),
            FOREIGN KEY(athlete) REFERENCES users(username)
        )
    ''')

    # Create performance table
    cursor_main.execute('''
        CREATE TABLE IF NOT EXISTS performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            athlete_id TEXT NOT NULL,
            date TEXT NOT NULL,
            stamina INTEGER CHECK(stamina BETWEEN 1 AND 10),
            strength INTEGER CHECK(strength BETWEEN 1 AND 10),
            speed INTEGER CHECK(speed BETWEEN 1 AND 10),
            focus INTEGER CHECK(focus BETWEEN 1 AND 10),
            injury_status TEXT DEFAULT 'None',
            notes TEXT,
            recorded_by TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(athlete_id) REFERENCES athletes(username)
        )
    ''')

    

    # Create injuries table
    cursor_main.execute('''
        CREATE TABLE IF NOT EXISTS injuries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            athlete_id TEXT NOT NULL,
            date_reported TEXT,
            injury_type TEXT,
            severity TEXT,
            expected_recovery TEXT,
            treatment TEXT,
            FOREIGN KEY(athlete_id) REFERENCES athletes(username)
        )
    ''')

    conn_main.commit()

    # Initialize enhanced features database
    conn_enhanced = sqlite3.connect(ENHANCED_DB_PATH, check_same_thread=False)
    cursor_enhanced = conn_enhanced.cursor()

    # Create goals table
    cursor_enhanced.execute('''
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            athlete_id TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            target_date TEXT,
            progress REAL DEFAULT 0,
            status TEXT DEFAULT 'In Progress',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(athlete_id) REFERENCES athletes(username)
        )
    ''')

    # Create contracts table
    cursor_enhanced.execute('''
        CREATE TABLE IF NOT EXISTS contracts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            athlete_id TEXT NOT NULL,
            contract_type TEXT,
            start_date TEXT,
            end_date TEXT,
            sponsor_name TEXT,
            earnings REAL DEFAULT 0,
            expenses REAL DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(athlete_id) REFERENCES athletes(username)
        )
    ''')

    conn_enhanced.commit()
    return conn_main, cursor_main, conn_enhanced, cursor_enhanced