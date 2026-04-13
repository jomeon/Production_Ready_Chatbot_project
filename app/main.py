from fastapi import FastAPI, HTTPException
from app.schemas import ChatRequest, ChatResponse
from app.session_manager import manager
import logging

app = FastAPI(
    title="APIS Chatbot API", 
    version="1.0.0", 
    description="Profesjonalne API Chatbota opartego o model LLM (Projekt APIS - Ocena 5.0)"
)


@app.get("/")
async def root():
    return {
        "message": "Witaj w API APIS Chatbot!", 
        "docs_url": "Przejdź pod /docs, aby testować API."
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Główny endpoint do komunikacji z chatbotem.
    Wymaga podania session_id (do śledzenia historii) oraz wiadomości.
    """
    try:
        # Obsługa sesji użytkownika
        bot = manager.get_or_create_session(request.session_id)
        
        # Generowanie odpowiedzi z przekazanymi parametrami (temperature, top_p)
        reply = bot.generate_response(
            user_message=request.message,
            temperature=request.temperature,
            top_p=request.top_p
        )
        
        return ChatResponse(session_id=request.session_id, reply=reply)
    
    except Exception as e:
        # Obsługa błędów API
        logging.error(f"Krytyczny błąd API w sesji {request.session_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Wewnętrzny błąd serwera. Sprawdź logi systemowe.")

@app.delete("/chat/{session_id}")
async def clear_session_endpoint(session_id: str):
    """
    Endpoint pomocniczy do resetowania historii rozmowy.
    """
    manager.clear_session(session_id)
    return {"message": f"Sesja {session_id} została wyczyszczona."}