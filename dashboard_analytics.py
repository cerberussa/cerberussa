import streamlit as st
import json
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Cerberussa Analytics", layout="centered")

st.title("📊 Booking Analytics Dashboard")

LOG_FILE = "bookings_log.json"

try:
    with open(LOG_FILE, "r") as f:
        bookings = json.load(f)
except FileNotFoundError:
    st.warning("No booking logs found yet.")
    bookings = []

if bookings:
    df = pd.DataFrame(bookings)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["service"] = df["service"].str.title()
    
    st.metric("📈 Total Bookings", len(df))
    
    urgent_count = df["data"].apply(lambda x: "now" in str(x).lower()).sum()
    st.metric("⚠️ Urgent Bookings", urgent_count)

    service_count = df["service"].value_counts()
    st.bar_chart(service_count)

    st.subheader("📋 Raw Booking Data")
    st.dataframe(df.tail(25))

    st.download_button("📥 Download CSV", data=df.to_csv(index=False), file_name="booking_stats.csv")

else:
    st.info("Waiting for the first bookings...")