"""
Chat endpoint implementation.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from pydantic import BaseModel, Field
import uuid

from .responses import ChatResponse
from ..services.agent_runner import AgentRunner
from ..core.logging import logger


router = APIRouter()


class ChatRequest(BaseModel):
    conversation_id: Optional[str] = Field(None, max_length=100)
    message: str = Field(..., min_length=1, max_length=10000)


class ChatResponseModel(BaseModel):
    conversation_id: str
    response: str
    tool_calls: list = []
    reasoning_trace: dict = {}


@router.post("/{user_id}/chat", response_model=ChatResponseModel)
async def chat(user_id: str, request: ChatRequest):
    """
    Chat endpoint that accepts user messages and returns responses from the LLM,
    potentially including tool calls to MCP tools.
    """
    try:
        # Validate user_id format (basic validation)
        if not user_id or len(user_id) > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "Validation failed",
                    "code": "VALIDATION_ERROR",
                    "details": {
                        "field": "user_id",
                        "message": "user_id must be between 1 and 100 characters"
                    }
                }
            )
        
        # Validate message
        if not request.message or len(request.message) < 1 or len(request.message) > 10000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "Validation failed",
                    "code": "VALIDATION_ERROR",
                    "details": {
                        "field": "message",
                        "message": "Message is required and must be between 1 and 10000 characters"
                    }
                }
            )
        
        # Validate conversation_id if provided
        if request.conversation_id:
            if len(request.conversation_id) > 100:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "error": "Validation failed",
                        "code": "VALIDATION_ERROR",
                        "details": {
                            "field": "conversation_id",
                            "message": "conversation_id must be 100 characters or less"
                        }
                    }
                )
        
        # Create AgentRunner instance
        agent_runner = AgentRunner()
        
        # Run the conversation
        result = await agent_runner.run_conversation(
            user_id=user_id,
            message=request.message,
            conversation_id=request.conversation_id
        )
        
        # Log the interaction
        logger.info(
            "Chat interaction completed",
            user_id=user_id,
            conversation_id=result["conversation_id"],
            message=request.message
        )
        
        # Return the response
        return ChatResponseModel(
            conversation_id=result["conversation_id"],
            response=result["response"],
            tool_calls=result.get("tool_calls", []),
            reasoning_trace=result.get("reasoning_trace", {})
        )
    
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Log the error
        logger.error("Error processing chat request", error=str(e), user_id=user_id)
        
        # Return a generic error response
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Internal server error",
                "code": "INTERNAL_ERROR",
                "details": {
                    "message": "An error occurred while processing your request"
                }
            }
        )