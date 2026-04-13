from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    session_id: str = Field(..., description="Unikalny identyfikator sesji użytkownika (np. user_123)")
    message: str = Field(..., min_length=1, description="Wiadomość od użytkownika")
    temperature: float = Field(default=0.7, ge=0.0, le=1.0, description="Kreatywność modelu (0.0 - 1.0)")
    top_p: float = Field(default=0.9, ge=0.0, le=1.0, description="Różnorodność słownictwa (0.0 - 1.0)")

class ChatResponse(BaseModel):
    session_id: str
    reply: str