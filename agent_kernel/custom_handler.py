from booking_logger import log_booking

def handle_custom(input_text, state={}):
    if not state.get("clarified"):
        return {
            "question": "Could you please tell us a bit more about what you need?",
            "booking": {"clarified": input_text},
            "complete": False
        }
    log_booking("custom", {"clarified_request": state.get("clarified"), "full_message": input_text})
    return {
        "message": f"Thanks! We'll escalate your request with Manageemnt and wil get back to you as soon as possible: \"{state.get('clarified')}\", to our manager right away.",
        "escalate": True,
        "complete": True
    }
