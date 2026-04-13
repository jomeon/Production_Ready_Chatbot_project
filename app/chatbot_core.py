import ollama
import logging
import os
from app.config import DEFAULT_MODEL_NAME, MAX_CONTEXT_MESSAGES

os.makedirs("logs", exist_ok=True)

# Konfiguracja logowania
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='logs/chatbot_errors.log',
    filemode='a'
)

class APISChatbot:
    def __init__(self, model_name: str = DEFAULT_MODEL_NAME, max_context_messages: int = MAX_CONTEXT_MESSAGES):
        """
        Inicjalizacja chatbota.
        :param model_name: Nazwa modelu (domyślnie lokalna Llama 3)
        :param max_context_messages: Kontrola kontekstu (sliding window)
        """
        self.model_name = model_name
        self.max_context_messages = max_context_messages
        
        self.system_prompt = {
            "role": "system", 
            "content": "Jesteś profesjonalnym i pomocnym asystentem AI. Odpowiadaj zwięźle, rzeczowo i zawsze w języku polskim."
        }
        
        self.history = [self.system_prompt]

    def _manage_context(self):
        """
        Wymóg 4.0: Kontrola długości kontekstu.
        Zostawia prompt systemowy i najnowsze wiadomości.
        """
        if len(self.history) > self.max_context_messages:
            self.history = [self.history[0]] + self.history[-(self.max_context_messages - 1):]

    def generate_response(self, user_message: str, temperature: float = 0.7, top_p: float = 0.9) -> str:
        """
        Generowanie odpowiedzi z obsługą parametrów i błędów 
        """
        self.history.append({"role": "user", "content": user_message})
        self._manage_context()

        try:
            response = ollama.chat(
                model=self.model_name,
                messages=self.history,
                options={
                    "temperature": temperature,
                    "top_p": top_p
                }
            )
            
            bot_reply = response['message']['content']
            self.history.append({"role": "assistant", "content": bot_reply})
            return bot_reply

        except Exception as e:
            error_msg = f"Błąd komunikacji z modelem {self.model_name}: {str(e)}"
            logging.error(error_msg)
            
            # Wycofaj wiadomość użytkownika w przypadku błędu, by nie psuć historii
            if self.history[-1]["role"] == "user":
                self.history.pop() 
            
            return "Przepraszam, napotkałem problem techniczny. Spróbuj ponownie za chwilę."