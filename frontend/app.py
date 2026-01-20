# frontend/app.py

import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Secure Internal Chatbot", layout="centered")

st.title("🔐 Secure Internal Company Chatbot")

# Session state
if "token" not in st.session_state:
    st.session_state.token = None

# ---------------- LOGIN ----------------
if st.session_state.token is None:
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        response = requests.post(
            f"{API_URL}/login",
            json={"username": username, "password": password},
        )

        if response.status_code == 200:
            st.session_state.token = response.json()["access_token"]
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials")

# ---------------- CHAT ----------------
else:
    st.subheader("Chat")

    query = st.text_input("Ask a question")

    if st.button("Send"):
        headers = {
            "Authorization": f"Bearer {st.session_state.token}"
        }

        response = requests.post(
            f"{API_URL}/chat",
            json={"query": query},
            headers=headers,
        )

        if response.status_code == 200:
            st.markdown("### 💬 Answer")
            st.write(response.json()["answer"])
        else:
            st.error("Access denied or error occurred")

    if st.button("Logout"):
        st.session_state.token = None
        st.rerun()
