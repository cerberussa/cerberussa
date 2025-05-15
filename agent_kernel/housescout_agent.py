from pydantic import BaseModel
from typing import Optional
from langgraph.graph import StateGraph, END
from booking_logger import log_booking

class HouseScoutRequest(BaseModel):
    name: str
    property_link: str
    questions: Optional[str]
    visit_time: str
    phone: str

def ask_for_fields(state):
    booking = state.get("booking", {})
    required = ["name", "property_link", "visit_time", "phone"]
    missing = [f for f in required if f not in booking or not booking[f]]
    if not missing:
        return {"booking": booking, "complete": True}

    questions = {
        "name": "Can I have your full name?",
        "property_link": "Please share the property link or address.",
        "questions": "Any specific questions you want us to ask?",
        "visit_time": "Preferred visit time or day?",
        "phone": "Your contact number, please."
    }
    next_field = missing[0]
    return {
        "question": questions[next_field],
        "missing_field": next_field,
        "booking": booking,
        "complete": False
    }

def confirm_booking(state):
    try:
        request = HouseScoutRequest(**state["booking"])
        log_booking("housing", request.dict())
        return {
            "message": f"✅ Property visit confirmed!\nLink: {request.property_link}\nTime: {request.visit_time}",
            "complete": True
        }
    except Exception as e:
        return {"message": f"❌ Error: {str(e)}", "complete": False}

def receive_input(state, input_text):
    field = state.get("missing_field")
    booking = state.get("booking", {})
    booking[field] = input_text
    return {"booking": booking}

graph = StateGraph()
graph.add_node("ask_for_fields", ask_for_fields)
graph.add_node("confirm_booking", confirm_booking)
graph.add_node("receive_input", receive_input)
graph.set_entry_point("ask_for_fields")
graph.add_edge("ask_for_fields", "confirm_booking")
graph.add_conditional_edges("confirm_booking", lambda s: "ask_for_fields" if not s.get("complete") else END)
graph.add_edge("receive_input", "ask_for_fields")
flow = graph.compile()

def run_agent(input_text, current_state={}):
    state = {**current_state, "input": input_text}
    return flow.invoke(state)