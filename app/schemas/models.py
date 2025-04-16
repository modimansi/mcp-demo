from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union

class Message(BaseModel):
    """Chat message model"""
    role: str = Field(..., description="Role of the message sender (user, assistant, system)")
    content: str = Field(..., description="Content of the message")
    
    class Config:
        schema_extra = {
            "example": {
                "role": "user",
                "content": "Hello, how can you help me today?"
            }
        }

class ChatRequest(BaseModel):
    """Chat request model"""
    messages: List[Message] = Field(..., description="List of previous messages in the conversation")
    stream: bool = Field(False, description="Whether to stream the response")
    
    class Config:
        schema_extra = {
            "example": {
                "messages": [
                    {
                        "role": "user",
                        "content": "Hello, how can you help me today?"
                    }
                ],
                "stream": False
            }
        }

class ChatResponse(BaseModel):
    """Chat response model"""
    message: Message = Field(..., description="Response message")
    
    class Config:
        schema_extra = {
            "example": {
                "message": {
                    "role": "assistant",
                    "content": "I'm an AI assistant and I'm here to help you with any questions or tasks you have!"
                }
            }
        }

class NodeRunInput(BaseModel):
    """Input for a LangGraph node run"""
    state: Dict[str, Any] = Field(..., description="Current state of the conversation")
    
class NodeRunOutput(BaseModel):
    """Output from a LangGraph node run"""
    state: Dict[str, Any] = Field(..., description="Updated state after the node execution")
    next: Optional[str] = Field(None, description="Next node to execute, if any")
