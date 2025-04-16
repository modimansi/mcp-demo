from fastapi import APIRouter, HTTPException, Depends
from app.schemas.models import ChatRequest, ChatResponse, Message
from app.graphs.conversation import get_conversation_graph
from typing import Dict, Any

router = APIRouter()

@router.get("/health")
async def health():
    """Health check endpoint for API"""
    return {"status": "ok"}

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a chat request and generate a response using LangGraph
    """
    try:
        # Initialize the conversation graph
        graph = get_conversation_graph()
        
        # Prepare the input for the graph
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        # Run the graph
        result = graph.invoke({
            "messages": messages,
            "stream": request.stream
        })
        
        # Extract the assistant's response
        assistant_message = result["messages"][-1]
        
        return ChatResponse(
            message=Message(
                role=assistant_message["role"],
                content=assistant_message["content"]
            )
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")

@router.get("/reset")
async def reset_conversation():
    """Reset the conversation state"""
    try:
        # Re-initialize the conversation graph
        get_conversation_graph(reset=True)
        return {"status": "conversation reset successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resetting conversation: {str(e)}")
