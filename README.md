# AI-Powered Bike Failure Diagnosis Assistant

## Overview

An AI-powered RAG chatbot that helps users troubleshoot common bike and scooter problems through interactive conversations. It uses **Google Gemini 2.5 Flash** and a custom troubleshooting knowledge base to ask relevant follow-up questions, identify possible faults, and recommend safe actions.

**Live Demo:** [Try the Bike Failure Diagnosis Assistant](https://22-bike-failure-diagnosis-assistant.vercel.app/)

## Key Features

- RAG-based troubleshooting using a custom knowledge base.
- Context-aware follow-up questions and multi-turn conversation memory.
- Structured Possible Diagnosis and Recommended Actions responses.
- Independent chat sessions with New Chat functionality.
- Safety-aware recommendations and API error handling.
- Interactive React interface with Markdown-formatted responses.

## Tech Stack

- **Languages:** Python, JavaScript
- **Frontend:** React, Vite, CSS
- **Backend:** FastAPI
- **LLM:** Google Gemini 2.5 Flash
- **Embeddings:** Google Gemini Embedding (`gemini-embedding-001`)
- **Vector Database:** ChromaDB
- **Framework:** LangChain
- **Deployment:** Render (Backend), Vercel (Frontend)

## How It Works

1. The user describes a bike or scooter problem through the React interface.
2. FastAPI manages the request and session-specific conversation history.
3. ChromaDB retrieves relevant troubleshooting information using semantic search.
4. Gemini generates follow-up questions, possible diagnoses, and recommended actions.
5. React displays the response in a conversational interface.

## Project Structure

```text
Bike-Failure-Diagnosis-Assistant/
├── main.py
├── chatbot.py
├── helper_func.py
├── Common bike problems- RAG.docx
├── chroma_db/
├── requirements.txt
├── README.md
└── frontend/
    ├── package.json
    └── src/
        ├── App.jsx
        └── App.css
```

## Run Locally

1. Install dependencies: `pip install -r requirements.txt`
2. Create a `.env` file with `GEMINI_API_KEY=your_api_key_here`
3. Start backend: `uvicorn main:app --reload`
4. Start frontend: `cd frontend`, `npm install`, `npm run dev`

**Note:** The frontend API URL must point to the backend being used.

## Disclaimer

This chatbot provides preliminary troubleshooting guidance and does not replace professional mechanical inspection or repair.