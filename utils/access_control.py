import streamlit as st

def login():
    """Simple login system using Streamlit secrets."""
    st.sidebar.title("🔐 Login")

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "role" not in st.session_state:
        st.session_state.role = None
    if "user" not in st.session_state:
        st.session_state.user = None

    if not st.session_state.authenticated:
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")

        if st.sidebar.button("Login"):
            valid_users = st.secrets["users"]
            if username in valid_users and password == valid_users[username]:
                st.session_state.authenticated = True
                st.session_state.user = username
                st.session_state.role = st.secrets["roles"].get(username, "Demo")
                st.sidebar.success(f"✅ Logged in as {username} ({st.session_state.role})")
                st.experimental_rerun()
            else:
                st.sidebar.error("❌ Invalid credentials")
        st.stop()

    # Logout button
    if st.sidebar.button("Logout"):
        for key in ["authenticated", "role", "user"]:
            if key in st.session_state:
                del st.session_state[key]
        st.sidebar.warning("Logged out.")
        st.experimental_rerun()

    return st.session_state.role
