from ollama import chat
from app.core.config import settings


def get_llama_response(conversation_id: int, chat_history: list) -> dict:
    try:
        system_prompt = {
            "role": "system",
            "content": (
                "You are a helpful, intelligent AI assistant. Always consider the full conversation history "
                "to maintain context, but respond specifically to the user's most recent message. "
                "Stay on topic, be concise, and clarify if something is unclear."
            ),
        }

        full_history = [system_prompt] + chat_history

        response = chat(model=settings.LLAMA_MODEL, messages=full_history)

        assistant_reply = response.get("message", {}).get("content", "").strip()

        if not assistant_reply:
            assistant_reply = "⚠️ LLaMA had nothing to say."

        updated_history = chat_history + [
            {"role": "assistant", "content": assistant_reply},
        ]

        return {
            "reply": assistant_reply,
            "updated_history": updated_history,
            "conversation_id": conversation_id,
        }

    except Exception as e:
        return {
            "reply": "❌ Error contacting LLaMA.",
            "updated_history": chat_history,
            "error": str(e),
        }
