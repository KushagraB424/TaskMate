import os
from google import genai
from google.genai import types

SYSTEM_PROMPT = """
You are TaskMates AI Assistant. You help users book home services like cleaning, plumbing, electrical work, beauty services, etc. You only answer queries related to services, bookings, pricing, or platform usage. You are polite, concise, and helpful. If the user asks unrelated questions, politely refuse.
"""

def get_gemini_response(session, user_message):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "Internal Error: Gemini API key is not configured."

    client = genai.Client(api_key=api_key)
    
    # Retrieve last 10 messages for context
    history_messages = session.messages.all().order_by('-timestamp')[:10]
    # Reverse to chronological order
    history_messages = list(history_messages)[::-1]
    
    # Format history for the new Gemini 2.5 SDK
    contents = []
    for msg in history_messages:
        if msg.message == user_message and msg.sender == 'USER':
             continue
        role = "user" if msg.sender == 'USER' else "model"
        contents.append(types.Content(role=role, parts=[types.Part.from_text(text=msg.message)]))
        
    contents.append(types.Content(role="user", parts=[types.Part.from_text(text=user_message)]))
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
            )
        )
        return response.text
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "Sorry, I am facing technical difficulties right now. Please try again later."
