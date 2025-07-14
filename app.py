import streamlit as st
import pandas as pd

# URL of the published Google Sheet CSV
sheet_url = 'https://docs.google.com/spreadsheets/d/1-vJ7GCem9qXCXDlJwflVgKFPdFgbjbQgoHiFoA76bHI/export?format=csv'

@st.cache_data(ttl=60)  # refresh every 60 seconds
def load_data():
    df = pd.read_csv(sheet_url)
    print(df)
    return df

st.title("🎟️ Live Auditorium Attendance")

df = load_data()

print('***************')
print(df)
print('***************')

if not df.empty:
    latest = df.iloc[-1]
    st.metric("Current Count", int(latest['Number']))
    st.caption(f"Last updated: {latest.get('Timestamp', 'N/A')}")

    st.line_chart(df['Number'])
else:
    st.warning("No data yet.")

if st.button("🔄 Refresh Now"):
    st.cache_data.clear()
    st.rerun()