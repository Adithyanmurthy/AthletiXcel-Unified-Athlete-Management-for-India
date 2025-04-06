import sqlite3

# Path to your SQLite database file
DB_PATH = "database.db"

# Connect to the database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

try:
    # Add the 'speed' column to the 'performance' table
    cursor.execute("""
        ALTER TABLE performance 
        ADD COLUMN speed INTEGER CHECK(speed BETWEEN 1 AND 10)
    """)
    print("Column 'speed' added successfully.")

    # Add the 'focus' column to the 'performance' table
    cursor.execute("""
        ALTER TABLE performance 
        ADD COLUMN focus INTEGER CHECK(focus BETWEEN 1 AND 10)
    """)
    print("Column 'focus' added successfully.")

    # Commit the changes
    conn.commit()

except sqlite3.OperationalError as e:
    # Handle errors (e.g., if the columns already exist)
    print(f"Error: {e}")

finally:
    # Close the connection
    conn.close()