import streamlit as st
import pandas as pd

def upload_contract(conn_enhanced, cursor_enhanced, athlete_id):
    st.subheader("Upload Contract Details")
    contract_type = st.text_input("Contract Type*")
    sponsor_name = st.text_input("Sponsor Name*")
    earnings = st.number_input("Earnings*", min_value=0.0, step=0.01)
    expenses = st.number_input("Expenses*", min_value=0.0, step=0.01)
    start_date = st.date_input("Start Date*")
    end_date = st.date_input("End Date*")

    if st.button("Save Contract"):
        try:
            cursor_enhanced.execute(
                """INSERT INTO contracts 
                (athlete_id, contract_type, sponsor_name, earnings, expenses, start_date, end_date) 
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (athlete_id, contract_type, sponsor_name, earnings, expenses, start_date, end_date)
            )
            conn_enhanced.commit()
            st.success("Contract saved successfully!")
        except Exception as e:
            st.error(f"Error: {str(e)}")