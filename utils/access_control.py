import streamlit as st

def login_screen():
    """Render login form and authenticate user."""
    st.markdown(
        """
        <style>
        div[data-testid="stSidebar"] {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("🔐 Innovation Mentor Login")
    st.write("Please sign in to continue.")

    # Initialize session states
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "role" not in st.session_state:
        st.session_state.role = None
    if "user" not in st.session_state:
        st.session_state.user = None

    # Centered layout
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_btn = st.button("Login")

        if login_btn:
            valid_users = st.secrets["users"]
            if username in valid_users and password == valid_users[username]:
                st.session_state.authenticated = True
                st.session_state.user = username
                st.session_state.role = st.secrets["roles"].get(username, "Demo")
                st.success(f"Welcome, {username}!")
                st.rerun()  # ✅ updated
            else:
                st.error("❌ Invalid username or password")

def logout_button():
    """Add logout button visible only after login."""
    if st.sidebar.button("Logout"):
        for k in ["authenticated", "user", "role"]:
            st.session_state.pop(k, None)
        st.sidebar.warning("Logged out.")
        st.rerun()  # ✅ updated
