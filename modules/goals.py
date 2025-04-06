import streamlit as st
import pandas as pd

def set_goal(conn_enhanced, cursor_enhanced, athlete_id):
    st.subheader("Set New Goal")
    with st.form("set_goal_form"):
        title = st.text_input("Goal Title*")
        description = st.text_area("Description")
        target_date = st.date_input("Target Date*")
        progress = st.slider("Progress (%)", 0, 100, 0)

        if st.form_submit_button("Save Goal"):
            try:
                cursor_enhanced.execute(
                    """INSERT INTO goals 
                    (athlete_id, title, description, target_date, progress) 
                    VALUES (?, ?, ?, ?, ?)""",
                    (athlete_id, title, description, target_date, progress)
                )
                conn_enhanced.commit()
                st.success("Goal saved successfully!")
            except Exception as e:
                st.error(f"Error: {str(e)}")