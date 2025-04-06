import sqlite3

# Path to your SQLite database file
DB_PATH = "database.db"

def fix_athletes_table():
    # Connect to the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Check if the 'sport' column exists in the 'athletes' table
        cursor.execute("PRAGMA table_info(athletes)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'sport' not in columns:
            print("Adding 'sport' column to the 'athletes' table...")
            cursor.execute("ALTER TABLE athletes ADD COLUMN sport TEXT DEFAULT 'Unknown'")
        
        if 'level' not in columns:
            print("Adding 'level' column to the 'athletes' table...")
            cursor.execute("ALTER TABLE athletes ADD COLUMN level TEXT DEFAULT 'Unknown'")
        
        # Commit the changes
        conn.commit()
        print("Database schema updated successfully.")

    except sqlite3.OperationalError as e:
        print(f"Error: {e}")

    finally:
        # Close the connection
        conn.close()

if __name__ == "__main__":
    fix_athletes_table()