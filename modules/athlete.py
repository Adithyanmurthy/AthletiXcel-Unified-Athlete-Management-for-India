import streamlit as st
import pandas as pd

def athlete_panel(conn_main, cursor_main, conn_enhanced, cursor_enhanced, athlete_username):
    st.title("Athlete Dashboard")
    
    # Get athlete info
    athlete_info = pd.read_sql_query(
        f"SELECT * FROM athletes WHERE username = '{athlete_username}'", 
        conn_main
    )
    
    if athlete_info.empty:
        st.error("Athlete profile not found!")
        return
    
    athlete_info = athlete_info.iloc[0]
    athlete_id = athlete_info['username']
    
    # Profile Header
    st.header(f"Welcome, {athlete_info['name']}")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Sport:** {athlete_info['sport']}")
        st.write(f"**Level:** {athlete_info['level']}")
    with col2:
        st.write(f"**Date of Birth:** {athlete_info['dob']}")
    
    # Performance Tab
    st.subheader("My Performance Metrics")
    
    # Get performance data
    performance = pd.read_sql_query(
        f"""SELECT date, stamina, strength, speed, focus, injury_status 
            FROM performance 
            WHERE athlete_id = '{athlete_id}'
            ORDER BY date DESC""", 
        conn_main
    )
    
    if not performance.empty:
        # Metrics Overview
        cols = st.columns(4)
        metrics = ['stamina', 'strength', 'speed', 'focus']
        for i, metric in enumerate(metrics):
            cols[i].metric(
                f"Avg {metric.capitalize()}", 
                round(performance[metric].mean(), 1))
        
        # Recent Records
        st.subheader("Recent Performance")
        st.dataframe(performance.head(5))
    else:
        st.info("No performance records available")
    
    # Goals Tab
    st.subheader("My Goals")
    goals = pd.read_sql_query(
        f"""SELECT title, description, target_date, progress 
            FROM goals 
            WHERE athlete_id = '{athlete_id}'""", 
        conn_enhanced
    )
    
    if not goals.empty:
        for _, goal in goals.iterrows():
            with st.expander(f"{goal['title']} ({goal['progress']}%)"):
                st.write(goal['description'])
                st.write(f"**Target Date:** {goal['target_date']}")
                st.progress(goal['progress'] / 100)
    else:
        st.info("No goals set yet")
    
    # Contracts Tab
    st.subheader("My Contracts")
    contracts = pd.read_sql_query(
        f"""SELECT contract_type, sponsor_name, earnings, expenses 
            FROM contracts 
            WHERE athlete_id = '{athlete_id}'""", 
        conn_enhanced
    )
    
    if not contracts.empty:
        st.dataframe(contracts)
    else:
        st.info("No contracts available")