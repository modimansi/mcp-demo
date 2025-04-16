from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from typing import Dict, List, Any, TypedDict, Annotated, Sequence, Union
from app.core.config import settings
import os
import json

# Define the state schema
class ConversationState(TypedDict):
    """State of the conversation graph"""
    messages: List[Dict[str, str]]  # List of messages exchanged
    stream: bool  # Whether to stream the response


# Define a reusable singleton pattern for the graph
_graph_instance = None

def get_conversation_graph(reset: bool = False) -> StateGraph:
    """
    Get a conversation graph instance. If reset is True, a new instance will be created.
    """
    global _graph_instance
    
    if _graph_instance is None or reset:
        _graph_instance = build_conversation_graph()
    
    return _graph_instance


def build_conversation_graph() -> StateGraph:
    """
    Build a LangGraph conversation graph
    """
    # Create a new graph
    graph = StateGraph(ConversationState)
    
    # Add nodes to the graph
    graph.add_node("generate_response", generate_response)
    
    # Add conditional edges
    graph.add_edge("generate_response", END)
    
    # Set the entry point
    graph.set_entry_point("generate_response")
    
    # Compile the graph
    return graph.compile()


def generate_response(state: ConversationState) -> ConversationState:
    """
    Generate a response using an LLM
    """
    # Extract messages from the state
    messages = state["messages"]
    
    # Initialize the LLM
    try:
        model = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=settings.DEFAULT_MODEL,
            temperature=0.7,
            streaming=state.get("stream", False),
        )
        
        # Generate a response
        response = model.invoke(messages)
        
        # Add the assistant's message to the conversation history
        if hasattr(response, "content"):
            assistant_message = {
                "role": "assistant",
                "content": response.content
            }
            messages.append(assistant_message)
        elif isinstance(response, dict) and "content" in response:
            assistant_message = {
                "role": "assistant",
                "content": response["content"]
            }
            messages.append(assistant_message)
        else:
            # Fallback for unexpected response format
            messages.append({
                "role": "assistant",
                "content": "I'm sorry, I encountered an issue with generating a response."
            })
        
        # Return the updated state
        return {"messages": messages, "stream": state.get("stream", False)}
    
    except Exception as e:
        # Handle errors
        print(f"Error generating response: {str(e)}")
        messages.append({
            "role": "assistant",
            "content": f"I'm sorry, I encountered an error: {str(e)}"
        })
        return {"messages": messages, "stream": state.get("stream", False)}
