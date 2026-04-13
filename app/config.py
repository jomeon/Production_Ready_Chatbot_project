import os

# Konfiguracja główna aplikacji
DEFAULT_MODEL_NAME = os.getenv("CHATBOT_MODEL", "llama3")
MAX_CONTEXT_MESSAGES = int(os.getenv("MAX_CONTEXT_MESSAGES", "10"))
DEFAULT_TEMPERATURE = 0.7
DEFAULT_TOP_P = 0.9