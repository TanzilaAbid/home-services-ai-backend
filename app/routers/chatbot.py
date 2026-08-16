from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.chat_service import handle_chat_message
 
router = APIRouter()
 
 
class ChatRequest(BaseModel):
    message: str
    user_id: str | None = None
    session_id: str | None = None
 
 
class ChatResponse(BaseModel):
    reply: str
    intent: dict
    matched_providers: list
    quick_replies: list
 
 
@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="message cannot be empty")
 
    try:
        result = handle_chat_message(request.message)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot error: {str(e)}")
 