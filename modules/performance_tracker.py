import streamlit as st
import pandas as pd

def daily_performance_tracker(conn_main, cursor_main, athlete_id):
    st.subheader("Daily Performance Tracker")
    with st.form("daily_performance_form"):
        date = st.date_input("Session Date*")
        stamina = st.slider("Stamina (1-10)*", 1, 10)
        strength = st.slider("Strength (1-10)*", 1, 10)
        focus = st.slider("Focus (1-10)*", 1, 10)
        injury_status = st.selectbox("Injury Status", ["None", "Minor", "Moderate", "Severe"])
        notes = st.text_area("Notes")

        if st.form_submit_button("Save Performance"):
            try:
                cursor_main.execute(
                    """INSERT INTO performance 
                    (athlete_id, date, stamina, strength, focus, injury_status, notes, recorded_by) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (athlete_id, date, stamina, strength, focus, injury_status, notes, "Self")
                )
                conn_main.commit()
                st.success("Performance logged successfully!")
            except Exception as e:
                st.error(f"Error: {str(e)}")