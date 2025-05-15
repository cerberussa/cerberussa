# model_router.py

def route_model(prompt: str) -> str:
    """
    Routes prompt to the most appropriate model.
    Returns: 'gpt' or 'claude'
    """
    prompt = prompt.lower()
    claude_keywords = ["plan", "schedule", "steps", "memory", "flow", "follow-up", "multi-step"]

    if any(kw in prompt for kw in claude_keywords) or len(prompt.split()) > 60:
        return "claude"
    
    return "gpt"
