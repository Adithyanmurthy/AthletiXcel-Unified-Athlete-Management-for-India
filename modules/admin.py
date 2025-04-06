import streamlit as st
import pandas as pd

def admin_panel(conn_main, cursor_main, conn_enhanced, cursor_enhanced):
    st.title("Admin Dashboard")

    tab1, tab2, tab3, tab4 = st.tabs(["👥 User Management", "📊 Performance Data", "🏥 Contract Entry", "📈 Analytics"])

    # User Management Tab
    with tab1:
        st.header("User Management")
        
        # Add New Athlete
        with st.expander("Add New Athlete"):
            with st.form("add_athlete_form", clear_on_submit=True):
                username = st.text_input("Username*", key="admin_add_athlete_username")
                password = st.text_input("Password*", type="password", key="admin_add_athlete_password")
                name = st.text_input("Full Name*", key="admin_add_athlete_name")
                dob = st.date_input("Date of Birth*", key="admin_add_athlete_dob")
                sport = st.text_input("Primary Sport*", key="admin_add_athlete_sport")
                level = st.selectbox("Level*", ["Beginner", "Intermediate", "Advanced", "Professional"], key="admin_add_athlete_level")
                
                submitted = st.form_submit_button("Add Athlete")  # No need for `key` here
                if submitted:
                    if not all([username, password, name, dob, sport, level]):
                        st.error("Please fill all required fields (*)")
                    else:
                        try:
                            cursor_main.execute(
                                "INSERT INTO users (username, password, role, name) VALUES (?, ?, ?, ?)",
                                (username, password, "Athlete", name)
                            )
                            cursor_main.execute(
                                """INSERT INTO athletes 
                                (username, name, dob, sport, level) 
                                VALUES (?, ?, ?, ?, ?)""",
                                (username, name, dob, sport, level)
                            )
                            conn_main.commit()
                            st.success(f"Athlete {name} added successfully!")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
        
        # Add New Coach
        with st.expander("Add New Coach"):
            with st.form("add_coach_form", clear_on_submit=True):
                username = st.text_input("Coach Username*", key="admin_add_coach_username")
                password = st.text_input("Password*", type="password", key="admin_add_coach_password")
                name = st.text_input("Full Name*", key="admin_add_coach_name")
                specialization = st.text_input("Specialization* (e.g., Strength, Endurance)", key="admin_add_coach_specialization")
                
                submitted = st.form_submit_button("Add Coach")  # No need for `key` here
                if submitted:
                    if not all([username, password, name, specialization]):
                        st.error("Please fill all required fields (*)")
                    else:
                        try:
                            cursor_main.execute(
                                "INSERT INTO users (username, password, role, name) VALUES (?, ?, ?, ?)",
                                (username, password, "Coach", name)
                            )
                            cursor_main.execute(
                                """INSERT INTO coaches 
                                (username, name, specialization) 
                                VALUES (?, ?, ?)""",
                                (username, name, specialization)
                            )
                            conn_main.commit()
                            st.success(f"Coach {name} added successfully!")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
        
        # Assign Coaches to Athletes
        with st.expander("Assign Coaches"):
            athletes = pd.read_sql_query("SELECT username, name FROM athletes", conn_main)
            coaches = pd.read_sql_query("SELECT username, name FROM coaches", conn_main)
            
            athlete = st.selectbox(
                "Select Athlete", 
                athletes['username'], 
                format_func=lambda x: athletes.loc[athletes['username'] == x, 'name'].values[0], 
                key="admin_assign_athlete"
            )
            coach = st.selectbox(
                "Select Coach", 
                coaches['username'], 
                format_func=lambda x: coaches.loc[coaches['username'] == x, 'name'].values[0], 
                key="admin_assign_coach"
            )
            
            if st.button("Assign Coach", key="admin_assign_submit"):
                try:
                    cursor_main.execute(
                        "INSERT INTO coach_assignments (coach, athlete) VALUES (?, ?)",
                        (coach, athlete)
                    )
                    conn_main.commit()
                    st.success(f"Assigned {coach} to {athlete}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    # Performance Data Tab
    with tab2:
        st.header("Performance Data Entry")
        
        # Select Athlete
        athletes = pd.read_sql_query("SELECT username, name FROM athletes", conn_main)
        selected_athlete = st.selectbox(
            "Select Athlete", 
            athletes['username'], 
            format_func=lambda x: athletes.loc[athletes['username'] == x, 'name'].values[0], 
            key="admin_performance_select_athlete"
        )
        
        # Add Performance Log
        with st.form("performance_form", clear_on_submit=True):
            date = st.date_input("Session Date*", key="admin_performance_date")
            
            col1, col2 = st.columns(2)
            with col1:
                stamina = st.slider("Stamina (1-10)*", 1, 10, key="admin_performance_stamina")
                strength = st.slider("Strength (1-10)*", 1, 10, key="admin_performance_strength")
            with col2:
                speed = st.slider("Speed (1-10)*", 1, 10, key="admin_performance_speed")
                focus = st.slider("Focus (1-10)*", 1, 10, key="admin_performance_focus")
            
            injury_status = st.selectbox("Injury Status", ["None", "Minor", "Moderate", "Severe"], key="admin_performance_injury")
            notes = st.text_area("Notes", key="admin_performance_notes")
            
            submitted = st.form_submit_button("Save Performance")  # No need for `key` here
            if submitted:
                try:
                    cursor_main.execute(
                        """INSERT INTO performance 
                        (athlete_id, date, stamina, strength, speed, focus, injury_status, notes, recorded_by) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (selected_athlete, date, stamina, strength, speed, focus, injury_status, notes, "Admin")
                    )
                    conn_main.commit()
                    st.success("Performance data saved!")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

        
    if submitted:
        # Save performance data
        cursor_main.execute(
            """INSERT INTO performance 
            (athlete_id, date, stamina, strength, speed, focus, injury_status, notes, recorded_by) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (selected_athlete, date, stamina, strength, speed, focus, injury_status, notes, "Admin")
        )
        conn_main.commit()

        # Update injury records
      #  update_injury_records(conn_main, cursor_main, selected_athlete, injury_status, date)


        
        
        






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
    


   

    # Contracts Tab
    with tab3:
        st.header("Upload Contract Details")
        athletes = pd.read_sql_query("SELECT username, name FROM athletes", conn_main)
        athlete = st.selectbox(
            "Select Athlete", 
            athletes['username'], 
            format_func=lambda x: athletes.loc[athletes['username'] == x, 'name'].values[0], 
            key="admin_contract_select_athlete"
        )
        
        contract_type = st.text_input("Contract Type*", key="admin_contract_type")
        sponsor_name = st.text_input("Sponsor Name*", key="admin_contract_sponsor")
        earnings = st.number_input("Earnings*", min_value=0.0, step=0.01, key="admin_contract_earnings")
        expenses = st.number_input("Expenses*", min_value=0.0, step=0.01, key="admin_contract_expenses")
        start_date = st.date_input("Start Date*", key="admin_contract_start_date")
        end_date = st.date_input("End Date*", key="admin_contract_end_date")
        
        if st.button("Save Contract", key="admin_contract_submit"):
            try:
                cursor_enhanced.execute(
                    """INSERT INTO contracts 
                    (athlete_id, contract_type, sponsor_name, earnings, expenses, start_date, end_date) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (athlete, contract_type, sponsor_name, earnings, expenses, start_date, end_date)
                )
                conn_enhanced.commit()
                st.success("Contract saved successfully!")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    # Analytics Tab
    with tab4:
        st.header("System Analytics")
        # Existing analytics implementation...