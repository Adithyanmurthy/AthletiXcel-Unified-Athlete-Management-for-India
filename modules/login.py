import streamlit as st
import pandas as pd

def login_screen(conn, cursor):
    st.title("🏅 Athlete Management System – India")
    choice = st.radio("Login or Signup?", ["Login", "Signup"])

    if choice == "Signup":
        st.subheader("🔐 Create New Account")
        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")
        role = st.selectbox("Select Role", ["Admin", "Coach", "Athlete"])
        if st.button("Create Account"):
            if new_user and new_pass:
                try:
                    cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                                   (new_user, new_pass, role))
                    conn.commit()
                    st.success(f"Account created! You can now login as {role}.")
                except:
                    st.error("Username already exists.")
            else:
                st.warning("Please enter all fields.")
    else:
        st.subheader("🔑 Login to Your Account")
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        if st.button("Login"):
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (user, pwd))
            data = cursor.fetchone()
            if data:
                st.session_state.logged_in = True
                st.session_state.username = user
                st.session_state.role = data[2]
                st.experimental_rerun()
            else:
                st.error("Invalid credentials.")