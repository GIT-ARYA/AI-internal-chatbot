import streamlit as st
import requests

# =============================
# Page Config
# =============================
st.set_page_config(
    page_title="Secure Internal Company Chatbot",
    page_icon="🔐",
    layout="centered",
)

st.title("🔐 Secure Internal Company Chatbot")

# =============================
# Load Backend URL from Secrets
# =============================
try:
    API_URL = "http://127.0.0.1:8000"
except KeyError:
    st.error("BACKEND_URL is not set in Streamlit secrets.")
    st.stop()

# Debug (you can remove later)
st.caption(f"Backend: {API_URL}")

# =============================
# Session State
# =============================
if "token" not in st.session_state:
    st.session_state.token = None

if "role" not in st.session_state:
    st.session_state.role = None

# =============================
# LOGIN UI
# =============================
if st.session_state.token is None:
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if not username or not password:
            st.warning("Please enter username and password.")
            st.stop()

        try:
            response = requests.post(
                f"{API_URL}/login",
                json={
                    "username": username,
                    "password": password,
                },
                timeout=10,
            )
        except Exception as e:
            st.error(f"❌ Cannot connect to backend: {e}")
            st.stop()

        if response.status_code == 200:
            data = response.json()
            st.session_state.token = data["access_token"]
            st.session_state.role = data["role"]
            st.success("✅ Login successful!")
            st.rerun()
        else:
            st.error("❌ Invalid credentials")

# =============================
# CHAT UI (After Login)
# =============================
else:
    st.success(f"Logged in as **{st.session_state.role}**")

    if st.button("Logout"):
        st.session_state.token = None
        st.session_state.role = None
        st.rerun()

    st.divider()
    st.subheader("💬 Internal Chat")

    user_query = st.text_input("Ask a question")

    if st.button("Send"):
        if not user_query.strip():
            st.warning("Please enter a question.")
            st.stop()

        headers = {
            "Authorization": f"Bearer {st.session_state.token}"
        }

        try:
            response = requests.post(
                f"{API_URL}/chat",
                json={"query": user_query},
                headers=headers,
                timeout=20,
            )
        except Exception as e:
            st.error(f"❌ Backend error: {e}")
            st.stop()

        if response.status_code == 200:
            result = response.json()
            st.markdown("### 🤖 Response")
            st.write(result["answer"])
        else:
            st.error("❌ You are not authorized or an error occurred.")
