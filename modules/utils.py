import streamlit as st
import pandas as pd
import sqlite3
import csv
import io

def export_data_button(cursor, table_name):
    """Create a button to export table data as CSV"""
    if st.button(f"Export {table_name} data"):
        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(columns)
        writer.writerows(data)
        
        # Create download button
        st.download_button(
            label="Download CSV",
            data=output.getvalue(),
            file_name=f"{table_name}.csv",
            mime="text/csv"
        )

def validate_date(date_str):
    """Basic date validation (format: YYYY-MM-DD)"""
    try:
        year, month, day = map(int, date_str.split('-'))
        return True
    except ValueError:
        return False

def display_athlete_table(cursor, search_query=None):
    """Display and return a filtered athlete table"""
    query = "SELECT * FROM athletes"
    params = []
    
    if search_query:
        query += " WHERE name LIKE ? OR sport LIKE ? OR level LIKE ?"
        params = [f"%{search_query}%"] * 3
    
    cursor.execute(query, params)
    athletes = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    
    if athletes:
        df = pd.DataFrame(athletes, columns=columns)
        return df
    else:
        st.info("No athletes found matching your search")
        return pd.DataFrame()

def backup_to_csv(cursor, table_name):
    """Backup SQLite table to CSV file"""
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        
        with open(f"data/{table_name}.csv", "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            writer.writerows(data)
            
        return True
    except Exception as e:
        st.error(f"Backup failed: {str(e)}")
        return False

def get_coach_options(cursor):
    """Return dictionary of {coach_username: coach_name}"""
    cursor.execute("SELECT username, name FROM users WHERE role='Coach'")
    return {row[0]: row[1] for row in cursor.fetchall()}

def get_athlete_options(cursor):
    """Return list of athlete usernames and names"""
    cursor.execute("SELECT username, name FROM athletes")
    return cursor.fetchall()

def format_date_for_display(date_str):
    """Convert YYYY-MM-DD to DD/MM/YYYY for display"""
    try:
        year, month, day = date_str.split('-')
        return f"{day}/{month}/{year}"
    except:
        return date_str

def display_success_message(message):
    """Standardized success message display"""
    st.success(message)
    st.toast(message, icon="✅")

def display_error_message(message):
    """Standardized error message display"""
    st.error(message)
    st.toast(message, icon="❌")