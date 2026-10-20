from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

# APIKey Loading:
load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")
client=genai.Client(api_key=api_key)

#1. Model generation:
def chat_with_model(messages, context='', model='gemini-2.5-flash',temperature=0):
    if context:
        messages = f"""Use the following retrieved context to help answer the user.
        Follow the conversation instructions provided in the message.
        Do NOT reply with just YES/NO.
        
        Context: {context}
        
        Message: {messages}"""

    response = client.models.generate_content(model=model, contents=messages, config=types.GenerateContentConfig(temperature=temperature))
    return response.text