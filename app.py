import streamlit as st
import pandas as pd
import datetime
import hashlib

st.set_page_config(layout="wide")

# =======================
# 1. AUTHENTICATION LAYER
# =======================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_credentials(username, password):
    try:
        stored_users = st.secrets["users"]
        return username in stored_users and stored_users[username] == hash_password(password)
    except Exception:
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

# ================
# 2. DASHBOARD APP
# ================

def attendance_dashboard():
    st.title("🎪 Sevan Startup Summit – Live Festival City Map")

    # --- Replace with your actual Google Sheets published CSV link! ---
    SHEET_URL_OCCUPANCY = "#"  # e.g., "https://docs.google.com/spreadsheets/d/your_sheet_id/export?format=csv"

    # --- Fallback to sample data if not yet linked ---
    @st.cache_data(ttl=60)
    def load_data():
        if SHEET_URL_OCCUPANCY.startswith("http"):
            df = pd.read_csv(SHEET_URL_OCCUPANCY)
        else:
            # Sample data structure, will be replaced by live data
            data = [
                {"zone_name": "Open-sky Aud", "attendance": 80, "session_title": "Panel 1", "speaker": "A. Mirzoyan", "rating": 4.5, "feedback": "Nice", "last_updated": "2025-07-16 12:00"},
                {"zone_name": "Mentorship", "attendance": 60, "session_title": "Mentor Time", "speaker": "S. Hakobyan", "rating": 4.8, "feedback": "Crowded", "last_updated": "2025-07-16 12:00"},
                {"zone_name": "Big Open Auditorium", "attendance": 120, "session_title": "Keynote", "speaker": "M. Khorasani", "rating": 4.9, "feedback": "Full", "last_updated": "2025-07-16 12:00"},
                {"zone_name": "Lake Side Hall", "attendance": 25, "session_title": "Fireside", "speaker": "N. Safaryan", "rating": 4.0, "feedback": "", "last_updated": "2025-07-16 12:00"},
                {"zone_name": "Open Aud 6", "attendance": 10, "session_title": "Workshop A", "speaker": "", "rating": 0, "feedback": "", "last_updated": "2025-07-16 12:00"},
                {"zone_name": "Open Aud 5", "attendance": 32, "session_title": "Workshop B", "speaker": "", "rating": 0, "feedback": "", "last_updated": "2025-07-16 12:00"},
                {"zone_name": "Open Aud 4", "attendance": 45, "session_title": "Session X", "speaker": "", "rating": 0, "feedback": "", "last_updated": "2025-07-16 12:00"},
                {"zone_name": "Big Hall", "attendance": 77, "session_title": "Main Event", "speaker": "", "rating": 4.6, "feedback": "", "last_updated": "2025-07-16 12:00"},
                {"zone_name": "Vision Hall", "attendance": 120, "session_title": "Vision Keynote", "speaker": "", "rating": 4.9, "feedback": "", "last_updated": "2025-07-16 12:00"},
                {"zone_name": "Open Aud 3", "attendance": 24, "session_title": "Startup Panel", "speaker": "", "rating": 4.2, "feedback": "", "last_updated": "2025-07-16 12:00"},
                {"zone_name": "Open Aud 2", "attendance": 44, "session_title": "Tech Demo", "speaker": "", "rating": 0, "feedback": "", "last_updated": "2025-07-16 12:00"},
                {"zone_name": "Open Aud 1", "attendance": 88, "session_title": "Pitch Battle", "speaker": "", "rating": 4.7, "feedback": "", "last_updated": "2025-07-16 12:00"},
                {"zone_name": "Unicorn Hall", "attendance": 57, "session_title": "VC Talk", "speaker": "", "rating": 4.3, "feedback": "", "last_updated": "2025-07-16 12:00"},
            ]
            df = pd.DataFrame(data)
        return df

    df = load_data()

    # --- Camp Fire Logic ---
    now = datetime.datetime.now()
    show_fire = (now.hour == 12)  # Fire between 20:00 and 21:00
    campfire_emoji = "🔥" if show_fire else "🪵"
    campfire_caption = "Camp Fire is 🔥 on!" if show_fire else "Camp Fire is off until 20:00"

    # --- CSS for Interactivity ---
    st.markdown("""
    <style>
    .zoneblock:hover {
        box-shadow: 0 0 20px 6px #7B68EE55;
        scale: 1.04;
        transition: 0.12s;
    }
    .zoneblock {
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)

    def zone_color(attendance):
        if attendance < 30:
            return "#A0A0A0"  # gray
        elif attendance <= 80:
            return "#FFEB3B"  # yellow
        else:
            return "#7B68EE"  # purple

    def glow_css(color):
        return f"0 0 20px 4px {color}55"

    def zone_button(name, attendance):
        color = zone_color(attendance)
        glow = glow_css(color)
        html = f"""
        <div class="zoneblock" style="
            background:{color};
            border-radius:24px;
            margin:8px 0;
            padding:26px 2px;
            box-shadow:{glow};
            text-align:center;
            font-weight:bold;
            font-size:1.3em;
            cursor:pointer;
            border: 3px solid #fff;
            ">
            {name}<br>
            <span style='font-size:1.1em;'>{attendance} <span style="font-size:0.8em;">people</span></span>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

    st.markdown("---")
    cols = st.columns([1.5, 1, 1, 1, 1, 1, 1.5])
    with cols[0]:
        st.markdown(f"""
            <div style="background:#222;border-radius:50px;padding:30px;text-align:center;font-size:2.2em;border:4px solid #7B68EE;box-shadow:0 0 18px #f90;">
                {campfire_emoji}
            </div>
            <div style="text-align:center;font-size:0.9em;margin-top:5px;color:#555;">Big Camp Fire<br><span style="font-size:0.8em">{campfire_caption}</span></div>
        """, unsafe_allow_html=True)
    with cols[1]: zone_button("Open-sky Aud", int(df.loc[df.zone_name=="Open-sky Aud","attendance"].values[0]))
    with cols[2]: zone_button("Mentorship", int(df.loc[df.zone_name=="Mentorship","attendance"].values[0]))
    with cols[3]: zone_button("Big Open Auditorium", int(df.loc[df.zone_name=="Big Open Auditorium","attendance"].values[0]))
    with cols[4]: zone_button("Lake Side Hall", int(df.loc[df.zone_name=="Lake Side Hall","attendance"].values[0]))
    with cols[5]: zone_button("Big Hall", int(df.loc[df.zone_name=="Big Hall","attendance"].values[0]))
    with cols[6]: zone_button("Vision Hall", int(df.loc[df.zone_name=="Vision Hall","attendance"].values[0]))

    cols2 = st.columns(6)
    with cols2[0]: zone_button("Open Aud 6", int(df.loc[df.zone_name=="Open Aud 6","attendance"].values[0]))
    with cols2[1]: zone_button("Open Aud 5", int(df.loc[df.zone_name=="Open Aud 5","attendance"].values[0]))
    with cols2[2]: zone_button("Open Aud 4", int(df.loc[df.zone_name=="Open Aud 4","attendance"].values[0]))
    with cols2[3]: zone_button("Open Aud 3", int(df.loc[df.zone_name=="Open Aud 3","attendance"].values[0]))
    with cols2[4]: zone_button("Open Aud 2", int(df.loc[df.zone_name=="Open Aud 2","attendance"].values[0]))
    with cols2[5]: zone_button("Open Aud 1", int(df.loc[df.zone_name=="Open Aud 1","attendance"].values[0]))

    st.markdown("---")
    st.markdown(
        "<div style='background:#e3e9f6;border-radius:22px;padding:16px;margin-top:18px;text-align:center;max-width:400px;margin:auto;'>"
        "Click any zone block above to see session details."
        "</div>", unsafe_allow_html=True
    )

    # --- Details sidebar ---
    zone_names = df["zone_name"].tolist()
    detailed_zone = st.selectbox("Or select a zone for details:", [""]+zone_names)
    if detailed_zone:
        zone = df[df.zone_name == detailed_zone].iloc[0]
        st.sidebar.title(f"📍 {zone.zone_name}")
        st.sidebar.write(f"**Session:** {zone.session_title}")
        st.sidebar.write(f"**Speaker:** {zone.speaker}")
        st.sidebar.write(f"**Attendance:** {zone.attendance}")
        st.sidebar.write(f"**Rating:** {zone.rating}")
        st.sidebar.write(f"**Feedback:** {zone.feedback}")
        st.sidebar.write(f"**Last Updated:** {zone.last_updated}")

    st.caption("Live auto-update and advanced interactivity can be added (e.g., live Google Sheet, direct block click events, live animation, etc.)")

    if st.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state.pop('username', None)
        st.rerun()

# =================
# 3. MAIN CONTROL
# =================

def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if st.session_state['logged_in']:
        attendance_dashboard()
    else:
        login_page()

if __name__ == "__main__":
    main()
    
# import streamlit as st
# import pandas as pd
# import datetime

# st.set_page_config(layout="wide")
# st.title("🎪 Sevan Startup Summit – Live Festival City Map")

# # -- Utility: Attendance to color/emoji logic --
# def zone_color(attendance):
#     if attendance < 30:
#         return "#A0A0A0"  # gray
#     elif attendance <= 80:
#         return "#FFEB3B"  # yellow
#     else:
#         return "#7B68EE"  # purple

# def glow_css(color):
#     return f"0 0 20px 4px {color}55"

# # -- Sample Data --
# data = [
#     {"zone_name": "Open-sky Aud", "attendance": 80, "session_title": "Panel 1", "speaker": "A. Mirzoyan", "rating": 4.5, "feedback": "Nice", "last_updated": "2025-07-16 12:00"},
#     {"zone_name": "Mentorship", "attendance": 60, "session_title": "Mentor Time", "speaker": "S. Hakobyan", "rating": 4.8, "feedback": "Crowded", "last_updated": "2025-07-16 12:00"},
#     {"zone_name": "Big Open Auditorium", "attendance": 120, "session_title": "Keynote", "speaker": "M. Khorasani", "rating": 4.9, "feedback": "Full", "last_updated": "2025-07-16 12:00"},
#     {"zone_name": "Lake Side Hall", "attendance": 25, "session_title": "Fireside", "speaker": "N. Safaryan", "rating": 4.0, "feedback": "", "last_updated": "2025-07-16 12:00"},
#     {"zone_name": "Open Aud 6", "attendance": 10, "session_title": "Workshop A", "speaker": "", "rating": 0, "feedback": "", "last_updated": "2025-07-16 12:00"},
#     {"zone_name": "Open Aud 5", "attendance": 32, "session_title": "Workshop B", "speaker": "", "rating": 0, "feedback": "", "last_updated": "2025-07-16 12:00"},
#     {"zone_name": "Open Aud 4", "attendance": 45, "session_title": "Session X", "speaker": "", "rating": 0, "feedback": "", "last_updated": "2025-07-16 12:00"},
#     {"zone_name": "Big Hall", "attendance": 77, "session_title": "Main Event", "speaker": "", "rating": 4.6, "feedback": "", "last_updated": "2025-07-16 12:00"},
#     {"zone_name": "Vision Hall", "attendance": 120, "session_title": "Vision Keynote", "speaker": "", "rating": 4.9, "feedback": "", "last_updated": "2025-07-16 12:00"},
#     {"zone_name": "Open Aud 3", "attendance": 24, "session_title": "Startup Panel", "speaker": "", "rating": 4.2, "feedback": "", "last_updated": "2025-07-16 12:00"},
#     {"zone_name": "Open Aud 2", "attendance": 44, "session_title": "Tech Demo", "speaker": "", "rating": 0, "feedback": "", "last_updated": "2025-07-16 12:00"},
#     {"zone_name": "Open Aud 1", "attendance": 88, "session_title": "Pitch Battle", "speaker": "", "rating": 4.7, "feedback": "", "last_updated": "2025-07-16 12:00"},
#     {"zone_name": "Unicorn Hall", "attendance": 57, "session_title": "VC Talk", "speaker": "", "rating": 4.3, "feedback": "", "last_updated": "2025-07-16 12:00"},
# ]
# df = pd.DataFrame(data)

# # --- Camp Fire Logic ---
# now = datetime.datetime.now()
# show_fire = (now.hour == 20)  # True between 20:00-21:00
# campfire_emoji = "🔥" if show_fire else "🪵"
# campfire_caption = "Camp Fire is 🔥 on!" if show_fire else "Camp Fire is off until 20:00"

# # --- Interactive Block Map Layout ---
# selected_zone = st.session_state.get("selected_zone", None)

# st.markdown("""
# <style>
# .zoneblock:hover {
#     box-shadow: 0 0 20px 6px #7B68EE55;
#     scale: 1.04;
#     transition: 0.12s;
# }
# .zoneblock {
#     cursor: pointer;
# }
# </style>
# """, unsafe_allow_html=True)

# def zone_button(name, attendance):
#     color = zone_color(attendance)
#     glow = glow_css(color)
#     html = f"""
#     <div class="zoneblock" style="
#         background:{color};
#         border-radius:24px;
#         margin:8px 0;
#         padding:26px 2px;
#         box-shadow:{glow};
#         text-align:center;
#         font-weight:bold;
#         font-size:1.3em;
#         cursor:pointer;
#         border: 3px solid #fff;
#         ">
#         {name}<br>
#         <span style='font-size:1.1em;'>{attendance} <span style="font-size:0.8em;">people</span></span>
#     </div>
#     """
#     return st.markdown(html, unsafe_allow_html=True)

# # ---- Map Rows ----

# st.markdown("---")

# cols = st.columns([1.5, 1, 1, 1, 1, 1, 1.5])
# with cols[0]:
#     st.markdown(f"""
#         <div style="background:#222;border-radius:50px;padding:30px;text-align:center;font-size:2.2em;border:4px solid #7B68EE;box-shadow:0 0 18px #f90;">
#             {campfire_emoji}
#         </div>
#         <div style="text-align:center;font-size:0.9em;margin-top:5px;color:#555;">Big Camp Fire<br><span style="font-size:0.8em">{campfire_caption}</span></div>
#     """, unsafe_allow_html=True)
# with cols[1]: zone_button("Open-sky Aud", df.loc[df.zone_name=="Open-sky Aud","attendance"].values[0])
# with cols[2]: zone_button("Mentorship", df.loc[df.zone_name=="Mentorship","attendance"].values[0])
# with cols[3]: zone_button("Big Open Auditorium", df.loc[df.zone_name=="Big Open Auditorium","attendance"].values[0])
# with cols[4]: zone_button("Lake Side Hall", df.loc[df.zone_name=="Lake Side Hall","attendance"].values[0])
# with cols[5]: zone_button("Big Hall", df.loc[df.zone_name=="Big Hall","attendance"].values[0])
# with cols[6]: zone_button("Vision Hall", df.loc[df.zone_name=="Vision Hall","attendance"].values[0])

# cols2 = st.columns(6)
# with cols2[0]: zone_button("Open Aud 6", df.loc[df.zone_name=="Open Aud 6","attendance"].values[0])
# with cols2[1]: zone_button("Open Aud 5", df.loc[df.zone_name=="Open Aud 5","attendance"].values[0])
# with cols2[2]: zone_button("Open Aud 4", df.loc[df.zone_name=="Open Aud 4","attendance"].values[0])
# with cols2[3]: zone_button("Open Aud 3", df.loc[df.zone_name=="Open Aud 3","attendance"].values[0])
# with cols2[4]: zone_button("Open Aud 2", df.loc[df.zone_name=="Open Aud 2","attendance"].values[0])
# with cols2[5]: zone_button("Open Aud 1", df.loc[df.zone_name=="Open Aud 1","attendance"].values[0])

# st.markdown("---")
# st.markdown(
#     "<div style='background:#e3e9f6;border-radius:22px;padding:16px;margin-top:18px;text-align:center;max-width:400px;margin:auto;'>"
#     "Click any zone block above to see session details."
#     "</div>", unsafe_allow_html=True
# )

# # --- Details sidebar ---
# zone_names = df["zone_name"].tolist()
# detailed_zone = st.selectbox("Or select a zone for details:", [""]+zone_names)
# if detailed_zone:
#     zone = df[df.zone_name == detailed_zone].iloc[0]
#     st.sidebar.title(f"📍 {zone.zone_name}")
#     st.sidebar.write(f"**Session:** {zone.session_title}")
#     st.sidebar.write(f"**Speaker:** {zone.speaker}")
#     st.sidebar.write(f"**Attendance:** {zone.attendance}")
#     st.sidebar.write(f"**Rating:** {zone.rating}")
#     st.sidebar.write(f"**Feedback:** {zone.feedback}")
#     st.sidebar.write(f"**Last Updated:** {zone.last_updated}")

# st.caption("Live auto-update and advanced interactivity can be added (e.g., live Google Sheet, direct block click events, live animation, etc.)")

# import streamlit as st
# import pandas as pd
# import hashlib

# # ------- Authentication Functions --------

# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()

# # Function to verify user credentials using secrets
# def verify_credentials(username, password):
#     # Access secrets from st.secrets
#     try:
#         stored_users = st.secrets["users"]
#         print(stored_users[username])
#         print(hash_password(password))
#         return username in stored_users and stored_users[username] == hash_password(password)
#     except KeyError:
#         st.error("Secrets configuration is missing!")
#         return False


# def login_page():
#     st.title("Login Page")
#     with st.form("login_form"):
#         username = st.text_input("Username")
#         password = st.text_input("Password", type="password")
#         submit_button = st.form_submit_button("Login")
#         if submit_button:
#             if verify_credentials(username, password):
#                 st.session_state['logged_in'] = True
#                 st.session_state['username'] = username
#                 st.success(f"Welcome {username}!")
#                 st.rerun()
#             else:
#                 st.error("Invalid username or password")

# # --------- Main Attendance App ----------

# def attendance_app():
#     st.title("🎟️ Live Auditorium Attendance")
#     sheet_url = "https://docs.google.com/spreadsheets/d/1-vJ7GCem9qXCXDlJwflVgKFPdFgbjbQgoHiFoA76bHI/export?format=csv"

#     @st.cache_data(ttl=60)
#     def load_data():
#         return pd.read_csv(sheet_url)

#     df = load_data()
#     if not df.empty:
#         latest = df.iloc[-1]
#         st.metric("Current Count", int(latest['Number']))
#         st.caption(f"Last updated: {latest.get('Timestamp', 'N/A')}")
#         st.line_chart(df['Number'])
#     else:
#         st.warning("No data yet.")

#     if st.button("Logout"):
#         st.session_state['logged_in'] = False
#         st.session_state.pop('username', None)
#         st.rerun()

# # ------------- Main Control -------------
# def main():
#     if 'logged_in' not in st.session_state:
#         st.session_state['logged_in'] = False

#     if st.session_state['logged_in']:
#         attendance_app()
#     else:
#         login_page()

# if __name__ == "__main__":
#     main()