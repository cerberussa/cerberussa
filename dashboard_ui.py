# dashboard_ui.py

import streamlit as st
import pandas as pd

st.set_page_config(page_title="DingDong Admin", layout="wide")
st.title("📋 DingDong Booking Dashboard")

# Dummy booking data for preview
bookings = [
    {"Service": "RideBuddy", "Client": "Laura M.", "Time": "Now", "Pickup": "Langstrasse 10", "Urgent": True, "Status": "Pending"},
    {"Service": "Cleaning", "Client": "Nina R.", "Time": "Tomorrow 9am", "Pickup": "Bahnofstrasse 22", "Urgent": False, "Status": "Confirmed"},
    {"Service": "HouseScout", "Client": "Maya T.", "Time": "Friday 3pm", "Pickup": "Online Listing", "Urgent": False, "Status": "Pending"},
]

df = pd.DataFrame(bookings)

# Filters
urgent_filter = st.selectbox("🔎 Show:", ["All", "Urgent Only", "Pending Only"])
if urgent_filter == "Urgent Only":
    df = df[df["Urgent"] == True]
elif urgent_filter == "Pending Only":
    df = df[df["Status"] == "Pending"]

st.dataframe(df, use_container_width=True)

# Booking actions
st.markdown("### ✅ Manage Booking")
selected_row = st.selectbox("Select Booking", df["Client"] + " - " + df["Service"])
status_update = st.radio("Update Status", ["Confirmed", "Cancelled", "In Progress"])
if st.button("Apply"):
    st.success(f"{selected_row} marked as {status_update}")
