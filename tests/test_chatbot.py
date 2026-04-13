import pytest
from app.chatbot_core import APISChatbot
from app.config import DEFAULT_MODEL_NAME

def test_bot_initialization():
    """Testuje, czy bot poprawnie się inicjalizuje i ładuje prompt systemowy."""
    bot = APISChatbot(model_name=DEFAULT_MODEL_NAME)
    assert len(bot.history) == 1
    assert bot.history[0]["role"] == "system"

def test_sliding_window_context_management():
    """Testuje mechanizm ucinania historii (Wymóg 4.0)."""
    # Inicjalizujemy bota z małym limitem kontekstu (3 wiadomości łącznie z systemowym)
    bot = APISChatbot(max_context_messages=3)
    
    # Symulujemy długą rozmowę
    bot.history.append({"role": "user", "content": "Wiadomość 1"})
    bot.history.append({"role": "assistant", "content": "Odpowiedź 1"})
    bot.history.append({"role": "user", "content": "Wiadomość 2"})
    bot.history.append({"role": "assistant", "content": "Odpowiedź 2"})
    
    # Odpalamy mechanizm ucinania
    bot._manage_context()
    
    # Sprawdzenia
    assert len(bot.history) == 3, "Historia powinna zostać ucięta do 3 wiadomości"
    assert bot.history[0]["role"] == "system", "Prompt systemowy musi zawsze zostać!"
    assert bot.history[-1]["content"] == "Odpowiedź 2", "Najnowsza wiadomość musi być na końcu"