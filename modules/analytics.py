import streamlit as st
import pandas as pd
import plotly.express as px

def analytics_dashboard(conn_main):
    st.title("Analytics Dashboard")

    # Fetch performance data
    performance = pd.read_sql_query(
        """SELECT a.name, p.date, p.stamina, p.strength, p.speed, p.focus 
           FROM performance p
           JOIN athletes a ON p.athlete_id = a.username
           ORDER BY p.date DESC""", 
        conn_main
    )

    if not performance.empty:
        # Generate a line chart for performance trends
        fig = px.line(
            performance, 
            x='date', 
            y=['stamina', 'strength', 'speed', 'focus'], 
            color='name',
            title="Performance Trends Over Time",
            labels={"value": "Metric Score", "date": "Date"}
        )
        st.plotly_chart(fig)
    else:
        st.info("No performance data available for analytics.")