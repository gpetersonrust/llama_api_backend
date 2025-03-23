from fastapi import APIRouter, Request
from app.models.chat_models import ChatRequest
from app.services import llama_service
from app.core.rate_limit import limiter  # ✅ Rate limiter

router = APIRouter(prefix="/v1", tags=["Chatbot"])


@router.post("/message")
@limiter.limit("5/minute")  # ⏳ Rate limit: 5 requests per minute per IP
async def receive_message(payload: ChatRequest, request: Request):
    """
    Receives user prompt and chat history, sends to LLaMA model,
    and returns the AI's response.
    """
    response = llama_service.get_llama_response(
        conversation_id=payload.conversation_id, chat_history=payload.chat_history
    )
    return response
