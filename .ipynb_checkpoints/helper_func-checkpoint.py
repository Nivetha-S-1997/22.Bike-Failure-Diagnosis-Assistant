import google.generativeai as genai

#1. Model generation:
def chat_with_model(messages, context='', model='gemini-2.5-flash',temperature=0,max_tokens=500):
    model_instance=genai.GenerativeModel(model)
    if context:
        messages = f"""Use the context to provide a FINAL DIAGNOSIS AND ACTION.
        Ask maximum 2 follow-up questions only if critical.
        Do NOT reply with just YES/NO.:\n{context}\n\n{messages}"""
    response=model_instance.generate_content(messages,generation_config={'temperature':temperature})
    return response.text

#2. Moderation check:
def moderation_check(user_text):
    prompt='''You are a moderation check assistant. Read the user's input.

    Respond with Y or N:
    Y- if the message contains harmful, violent, sexual, hateful, unsafe content.
    N- if otherwise.
    
    user_message="{msg}"'''.replace("{msg}",user_text)

    messages=[
        {'role':'user','parts':[{'text':prompt}]}
    ]

    mod_response=chat_with_model(messages,max_tokens=1).strip().upper()
    return mod_response