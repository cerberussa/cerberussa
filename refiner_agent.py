from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DEFAULT_PROMPT = """
You are a friendly Swiss concierge assistant. Your job is to understand customer requests and help them complete a booking for a predefined service: RideBuddy, HouseScout, Errands, Cleaning or Custom.

Be natural, polite, efficient. Avoid repeating too much or offering services outside the predefined list.
"""

def refine_prompt(feedback: str, current_prompt: str = DEFAULT_PROMPT) -> str:
    messages = [
        {"role": "system", "content": "You are a prompt improvement assistant."},
        {"role": "user", "content": f"Here's a current system prompt:

{current_prompt}

Now improve it based on this feedback:

{feedback}"}
    ]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.3
    )

    return response.choices[0].message.content.strip()

# Example:
# improved = refine_prompt("Too robotic, make it more human.")
# print(improved)