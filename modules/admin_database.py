# modules/admin_database.py
import sqlite3
import pandas as pd
import os

ADMIN_DB_PATH = "admin_inputs.db"

def init_admin_db():
    if not os.path.exists(ADMIN_DB_PATH):
        conn = sqlite3.connect(ADMIN_DB_PATH, check_same_thread=False)
        cursor = conn.cursor()

        # Athlete Performance Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS athlete_performance (
                athlete_id INTEGER,
                date TEXT,
                stamina INTEGER,
                strength INTEGER,
                speed INTEGER,
                focus INTEGER,
                injury_status TEXT,
                notes TEXT,
                recorded_by TEXT
            )
        ''')

        # Athlete Goals Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS athlete_goals (
                athlete_id INTEGER,
                title TEXT,
                description TEXT,
                target_date TEXT,
                status TEXT,
                progress INTEGER
            )
        ''')

        # Coach Assignments Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS coach_assignments (
                coach_username TEXT,
                athlete_username TEXT,
                assignment_details TEXT,
                start_date TEXT,
                end_date TEXT
            )
        ''')

        # Coach Training Plans Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS coach_training_plans (
                coach_username TEXT,
                plan_name TEXT,
                description TEXT,
                start_date TEXT,
                end_date TEXT,
                assigned_to TEXT
            )
        ''')

        conn.commit()
        return conn, cursor
    else:
        return sqlite3.connect(ADMIN_DB_PATH, check_same_thread=False), None