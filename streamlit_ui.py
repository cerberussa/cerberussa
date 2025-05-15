# streamlit_ui.py

import streamlit as st
from agent_kernel import (
    ridebuddy_agent, housescout_agent,
    errands_agent, cleaning_agent, custom_handler
)

st.set_page_config(page_title="Cerberussa", layout="centered")
st.title("🧠 Cerberussa Agent Interface")

AGENTS = {
    "RideBuddy": ridebuddy_agent.run_agent,
    "HouseScout": housescout_agent.run_agent,
    "Errands & Delivery": errands_agent.run_agent,
    "House Cleaning": cleaning_agent.run_agent,
    "Custom / Escalation": custom_handler.handle_custom,
}

agent_choice = st.selectbox("Select Assistant", list(AGENTS.keys()))
user_input = st.text_input("What would you like to say?", "")

if st.button("Send"):
    with st.spinner("Thinking..."):
        response = AGENTS[agent_choice](user_input)
        st.success(response["message"] if isinstance(response, dict) else response)
