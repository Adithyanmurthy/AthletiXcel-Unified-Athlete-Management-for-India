import streamlit as st
from modules.database import init_db
from modules.login import login_screen
from modules.admin import admin_panel
from modules.coach import coach_panel
from modules.athlete import athlete_panel

# Initialize DB
conn_main, cursor_main, conn_enhanced, cursor_enhanced = init_db()

# Session setup
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ''
    st.session_state.role = ''

# Login/Signup
if not st.session_state.logged_in:
    login_screen(conn_main, cursor_main)
else:
    role = st.session_state.role
    st.sidebar.title(f"Welcome {st.session_state.username} ({role})")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if role == "Admin":
        admin_panel(conn_main, cursor_main, conn_enhanced, cursor_enhanced)
    elif role == "Coach":
        # Pass only the required arguments
        coach_panel(conn_main, cursor_main, conn_enhanced, st.session_state.username)
    elif role == "Athlete":
        athlete_panel(conn_main, cursor_main, conn_enhanced, cursor_enhanced, st.session_state.username)