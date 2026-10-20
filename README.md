# AI-Powered Bike Failure Diagnosis Assistant

## Overview
An AI-powered chatbot that helps users diagnose common bike and scooter problems through interactive conversations. It uses **Retrieval-Augmented Generation (RAG)** and **Google Gemini 2.5 Flash** to retrieve relevant troubleshooting information, ask follow-up questions, and suggest possible diagnoses and actions.

## Key Features
- RAG-based troubleshooting using a custom knowledge base.
- Multi-turn conversations with context-aware follow-up questions.
- Independent chat sessions with New Chat functionality.
- AI-generated diagnoses and recommended actions.
- Safety instructions and API error handling.
- Interactive React interface with formatted responses.

## Tech Stack
- **Language:** Python, JavaScript
- **Frontend:** React, CSS, Vite
- **Backend:** FastAPI
- **LLM:** Google Gemini 2.5 Flash (Google Gen AI SDK)
- **Embeddings:** Hugging Face `all-MiniLM-L6-v2`
- **Vector Database:** ChromaDB
- **Framework:** LangChain

## How It Works
1. The user describes a bike or scooter issue through the React interface.
2. FastAPI processes the message and maintains session-specific conversation history.
3. ChromaDB retrieves relevant information from the troubleshooting knowledge base using semantic search.
4. Gemini generates context-aware follow-up questions, possible diagnoses, and recommended actions.
5. The response is displayed in the React chat interface.

## Project Structure
```text
Bike-Failure-Diagnosis-Assistant/
├── main.py
├── chatbot.py
├── helper_func.py
├── Common bike problems- RAG.docx
├── requirements.txt
├── README.md
└── frontend/
    ├── package.json
    ├── src/
    │   ├── App.jsx
    │   └── App.css
    └── ...
```

## Installation and Setup

**1. Install backend dependencies**
```bash
pip install -r requirements.txt
```

**2. Configure Gemini API key**

Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_api_key_here
```

**3. Start FastAPI**
```bash
uvicorn main:app --reload
```

**4. Start React**

Open another terminal:
```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` to use the chatbot.

## Disclaimer
This chatbot provides preliminary troubleshooting suggestions and does not replace professional mechanical inspection or repair.