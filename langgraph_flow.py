# langgraph_flow.py

from langgraph.graph import StateGraph, END

def build_flow(ask_fn, validate_fn, input_fn):
    """
    Returns a compiled LangGraph flow for an assistant.
    ask_fn: function to ask for missing fields
    validate_fn: function to validate booking
    input_fn: function to update booking state
    """
    graph = StateGraph()
    graph.add_node("ask_for_fields", ask_fn)
    graph.add_node("confirm_booking", validate_fn)
    graph.add_node("receive_input", input_fn)

    graph.set_entry_point("ask_for_fields")
    graph.add_edge("ask_for_fields", "confirm_booking")
    graph.add_conditional_edges("confirm_booking", lambda s: "ask_for_fields" if not s.get("complete") else END)
    graph.add_edge("receive_input", "ask_for_fields")

    return graph.compile()
