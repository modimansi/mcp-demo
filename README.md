# MCP Demo

A demonstration project featuring FastAPI, LangGraph, and a basic UI.

## Overview

This project demonstrates how to build an AI-powered application using:

- **FastAPI**: A modern, fast web framework for building APIs
- **LangGraph**: A library for building stateful, multi-actor applications with LLMs
- **Basic UI**: A simple frontend to interact with the API

## Project Structure

```
mcp-demo/
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py      # API endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py      # Configuration settings
│   ├── graphs/
│   │   ├── __init__.py
│   │   └── conversation.py # LangGraph implementation
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── models.py      # Pydantic models
│   └── static/
│       ├── css/
│       │   └── styles.css
│       ├── js/
│       │   └── app.js
│       └── index.html     # Simple UI
├── requirements.txt
└── README.md
```

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/modimansi/mcp-demo.git
   cd mcp-demo
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

4. Open your browser and navigate to http://localhost:8000

## API Endpoints

- `GET /`: UI interface
- `GET /api/health`: Health check endpoint
- `POST /api/chat`: Send a message to the LangGraph conversation

## Requirements

- Python 3.9+
- FastAPI
- LangGraph
- Uvicorn
- Additional dependencies listed in requirements.txt
