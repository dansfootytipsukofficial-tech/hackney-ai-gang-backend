from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.utils.ai_model import AIModel

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 1000
    conversation_history: Optional[List[dict]] = None

class ChatResponse(BaseModel):
    response: str
    model_used: str

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        response = await AIModel.generate_response(
            message=request.message,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            conversation_history=request.conversation_history
        )

        return ChatResponse(
            response=response,
            model_used=request.model
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")