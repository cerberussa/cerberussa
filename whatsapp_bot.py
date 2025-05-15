# whatsapp_bot.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from agent_kernel import (
    ridebuddy_agent, housescout_agent,
    errands_agent, cleaning_agent, custom_handler
)

from model_router import route_model

# Local session tracking
user_sessions = {}

# WhatsApp launch config
options = Options()
options.add_argument("--user-data-dir=/home/ubuntu/.config/google-chrome")
options.add_argument("--profile-directory=Default")

driver = webdriver.Chrome(options=options)
driver.get("https://web.whatsapp.com")
print(">> Please scan QR if not logged in...")

# Wait for chat interface
time.sleep(15)

def detect_new_message():
    try:
        messages = driver.find_elements(By.XPATH, '//div[@data-testid="msg-container"]')
        last_msg = messages[-1].text.strip()
        return last_msg
    except:
        return None

def send_reply(text):
    input_box = driver.find_element(By.XPATH, '//div[@title="Type a message"]')
    input_box.click()
    input_box.send_keys(text)
    input_box.send_keys("\n")

def handle_message(user_id, msg):
    if user_id not in user_sessions:
        user_sessions[user_id] = {
            "service": ridebuddy_agent.run_agent,
            "state": {},
        }

    session = user_sessions[user_id]
    reply = session["service"](msg, session["state"])
    if isinstance(reply, dict):
        user_sessions[user_id]["state"] = reply.get("booking", {})
        return reply.get("question") or reply.get("message")
    else:
        return reply

# Main loop
last_msg = ""
while True:
    try:
        msg = detect_new_message()
        if msg and msg != last_msg:
            print("User:", msg)
            reply = handle_message("user1", msg)
            print("Bot:", reply)
            send_reply(reply)
            last_msg = msg
        time.sleep(5)
    except Exception as e:
        print("Error:", e)
        time.sleep(5)
