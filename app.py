import streamlit as st
import pandas as pd
import hashlib

# ------- Authentication Functions --------

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to verify user credentials using secrets
def verify_credentials(username, password):
    # Access secrets from st.secrets
    try:
        stored_users = st.secrets["users"]
        print(stored_users[username])
        print(hash_password(password))
        return username in stored_users and stored_users[username] == hash_password(password)
    except KeyError:
        st.error("Secrets configuration is missing!")
        return False


def login_page():
    st.title("Login Page")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
        if submit_button:
            if verify_credentials(username, password):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.success(f"Welcome {username}!")
                st.rerun()
            else:
                st.error("Invalid username or password")

# --------- Main Attendance App ----------

def attendance_app():
    st.title("🎟️ Live Auditorium Attendance")
    sheet_url = "https://docs.google.com/spreadsheets/d/1-vJ7GCem9qXCXDlJwflVgKFPdFgbjbQgoHiFoA76bHI/export?format=csv"

    @st.cache_data(ttl=60)
    def load_data():
        return pd.read_csv(sheet_url)

    df = load_data()
    if not df.empty:
        latest = df.iloc[-1]
        st.metric("Current Count", int(latest['Number']))
        st.caption(f"Last updated: {latest.get('Timestamp', 'N/A')}")
        st.line_chart(df['Number'])
    else:
        st.warning("No data yet.")

    if st.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state.pop('username', None)
        st.rerun()

# ------------- Main Control -------------
def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state['logged_in']:
        attendance_app()
    else:
        login_page()

if __name__ == "__main__":
    main()