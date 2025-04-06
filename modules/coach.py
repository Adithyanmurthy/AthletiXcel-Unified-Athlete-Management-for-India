import streamlit as st
import pandas as pd

def update_injury_records(conn_main, cursor_main, athlete_id, injury_status, date):
    if injury_status != "None":
        try:
            cursor_main.execute(
                """INSERT INTO injuries (athlete_id, date_reported, injury_type, severity, expected_recovery, treatment)
                   VALUES (?, ?, ?, ?, ?, ?)
                   ON CONFLICT(athlete_id, date_reported) DO UPDATE SET
                   injury_type = excluded.injury_type,
                   severity = excluded.severity""",
                (athlete_id, date, injury_status, "Moderate", "2 weeks", "Rest and recovery")
            )
            conn_main.commit()
        except Exception as e:
            st.error(f"Error updating injury records: {str(e)}")

def coach_panel(conn_main, cursor_main, conn_enhanced, coach_username):
    st.title("Coach Dashboard")

    # Fetch assigned athletes
    assigned_athletes = pd.read_sql_query(
        f"""SELECT a.username, a.name, a.sport, a.level 
            FROM athletes a
            JOIN coach_assignments ca ON a.username = ca.athlete
            WHERE ca.coach = '{coach_username}'""",
        conn_main
    )

    # Handle missing columns gracefully
    if 'sport' not in assigned_athletes.columns:
        assigned_athletes['sport'] = "Unknown"
    if 'level' not in assigned_athletes.columns:
        assigned_athletes['level'] = "Unknown"

    # Display assigned athletes
    if not assigned_athletes.empty:
        st.subheader("Assigned Athletes")
        st.dataframe(assigned_athletes[['name', 'sport', 'level']])
    else:
        st.info("No athletes assigned to this coach.")

    # Select an athlete to view or log performance
    selected_athlete = st.selectbox(
        "Select Athlete",
        assigned_athletes['username'],
        format_func=lambda x: assigned_athletes.loc[assigned_athletes['username'] == x, 'name'].values[0],
        key="coach_select_athlete"
    )

    # Performance Data Entry
    with st.expander("Log Performance Data"):
        with st.form("performance_form", clear_on_submit=True):
            date = st.date_input("Session Date*", key="coach_performance_date")
            
            col1, col2 = st.columns(2)
            with col1:
                stamina = st.slider("Stamina (1-10)*", 1, 10, key="coach_performance_stamina")
                strength = st.slider("Strength (1-10)*", 1, 10, key="coach_performance_strength")
            with col2:
                speed = st.slider("Speed (1-10)*", 1, 10, key="coach_performance_speed")
                focus = st.slider("Focus (1-10)*", 1, 10, key="coach_performance_focus")
            
            injury_status = st.selectbox("Injury Status", ["None", "Minor", "Moderate", "Severe"], key="coach_performance_injury")
            notes = st.text_area("Notes", key="coach_performance_notes")
            
            submitted = st.form_submit_button("Save Performance")
            if submitted:
                try:
                    cursor_main.execute(
                        """INSERT INTO performance 
                        (athlete_id, date, stamina, strength, speed, focus, injury_status, notes, recorded_by) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (selected_athlete, date, stamina, strength, speed, focus, injury_status, notes, coach_username)
                    )
                    conn_main.commit()
                    
                    # Update injury records
                    update_injury_records(conn_main, cursor_main, selected_athlete, injury_status, date)
                    
                    st.success("Performance data saved successfully!")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    # View Performance History
    st.subheader("Performance History")
    performance = pd.read_sql_query(
        f"""SELECT date, stamina, strength, speed, focus, injury_status, notes 
            FROM performance 
            WHERE athlete_id = '{selected_athlete}'
            ORDER BY date DESC""", 
        conn_main
    )
    
    if not performance.empty:
        st.dataframe(performance)
    else:
        st.info("No performance records available")