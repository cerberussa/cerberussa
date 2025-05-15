from agent_kernel import ridebuddy_agent, housescout_agent, errands_agent, cleaning_agent, custom_handler

AGENT_MAP = {
    "ridebuddy": ridebuddy_agent.run_agent,
    "housing": housescout_agent.run_agent,
    "errands": errands_agent.run_agent,
    "cleaning": cleaning_agent.run_agent,
    "custom": custom_handler.handle_custom
}

def launch_agent(service_key, user_input, state={}):
    agent = AGENT_MAP.get(service_key)
    if not agent:
        return {"message": f"Unknown service: {service_key}"}
    return agent(user_input, state)