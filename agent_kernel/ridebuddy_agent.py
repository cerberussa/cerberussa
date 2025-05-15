from pydantic import BaseModel
from typing import Optional
from langgraph.graph import StateGraph, END
from booking_logger import log_booking

class RideBuddyBooking(BaseModel):
    name: str
    pickup: str
    dropoff: str
    time: str
    return_ride: Optional[bool] = False
    notes: Optional[str] = None

def ask_for_missing_fields(state):
    booking = state.get("booking", {})
    missing = [f for f in RideBuddyBooking.__fields__ if f not in booking or not booking[f]]
    if not missing:
        return {"booking": booking, "complete": True}
    questions = {
        "name": "May I have your full name, please?",
        "pickup": "Where should we pick you up from?",
        "dropoff": "And where are we dropping you off?",
        "time": "What time should we schedule the ride? (Now, 30 min, custom)",
        "return_ride": "Do you also need a return ride?",
        "notes": "Anything else we should be aware of?"
    }
    next_field = missing[0]
    return {"question": questions[next_field], "missing_field": next_field, "booking": booking, "complete": False}

def validate_booking(state):
    try:
        booking = RideBuddyBooking(**state["booking"])
        log_booking("ridebuddy", booking.dict())
        return {
            "message": f"✅ Ride confirmed!\nPickup: {booking.pickup}\nDropoff: {booking.dropoff}\nTime: {booking.time}",
            "complete": True
        }
    except Exception as e:
        return {"message": f"❌ Validation failed: {str(e)}", "complete": False}

def receive_input(state, input_text):
    field = state.get("missing_field")
    booking = state.get("booking", {})
    booking[field] = input_text
    return {"booking": booking}

graph = StateGraph()
graph.add_node("ask_for_fields", ask_for_missing_fields)
graph.add_node("validate_booking", validate_booking)
graph.add_node("receive_input", receive_input)
graph.set_entry_point("ask_for_fields")
graph.add_edge("ask_for_fields", "validate_booking")
graph.add_conditional_edges("validate_booking", lambda s: "ask_for_fields" if not s.get("complete") else END)
graph.add_edge("receive_input", "ask_for_fields")
flow = graph.compile()

def run_agent(input_text, current_state={}):
    state = {**current_state, "input": input_text}
    return flow.invoke(state)