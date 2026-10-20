from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.api_core.exceptions import ResourceExhausted, GoogleAPICallError
from pydantic import BaseModel
from uuid import uuid4
from chatbot import process_user_message

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: str

@app.get("/")
def home():
    return {"message": "Bike Failure Diagnosis API is running!"}

@app.post("/new-chat")
def new_chat():
    session_id = str(uuid4())
    return {"session_id": session_id}

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        if not request.message.strip():
            raise HTTPException(
                status_code=400,
                detail="Please enter a message."
            )

        response = process_user_message(
            request.message,
            request.session_id
        )

        return {"response": response}

    except HTTPException:
        raise

    except ResourceExhausted:
        raise HTTPException(
            status_code=429,
            detail="The chatbot has reached its AI usage limit. Please try again later."
        )

    except GoogleAPICallError:
        raise HTTPException(
            status_code=503,
            detail="The AI service is temporarily unavailable. Please try again later."
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again later."
        )