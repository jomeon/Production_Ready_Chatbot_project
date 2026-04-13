from app.chatbot_core import APISChatbot
from typing import Dict
from app.config import DEFAULT_MODEL_NAME


class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, APISChatbot] = {}

    def get_or_create_session(self, session_id: str) -> APISChatbot:
        """
        Zwraca instancję chatbota dla danej sesji. 
        Jeśli sesja nie istnieje, tworzy nową, izolowaną historię.
        """
        if session_id not in self.sessions:
            self.sessions[session_id] = APISChatbot(model_name=DEFAULT_MODEL_NAME)
        
        return self.sessions[session_id]

    def clear_session(self, session_id: str):
        """Opcjonalna metoda do czyszczenia pamięci, gdy użytkownik kończy rozmowę."""
        if session_id in self.sessions:
            del self.sessions[session_id]

manager = SessionManager()