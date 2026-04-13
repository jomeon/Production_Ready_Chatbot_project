import pytest
from app.chatbot_core import APISChatbot

def test_sliding_window_context_management():
    # Inicjalizujemy bota z małym limitem kontekstu (np. 3 wiadomości łącznie z systemowym)
    bot = APISChatbot(max_context_messages=3)
    
    # Symulujemy długą rozmowę
    bot.history.append({"role": "user", "content": "Wiadomość 1"})
    bot.history.append({"role": "assistant", "content": "Odpowiedź 1"})
    bot.history.append({"role": "user", "content": "Wiadomość 2"})
    bot.history.append({"role": "assistant", "content": "Odpowiedź 2"})
    
    # Odpalamy mechanizm ucinania
    bot._manage_context()
    
    # Sprawdzenia (Aserty)
    assert len(bot.history) == 3, "Historia powinna mieć dokładnie 3 wiadomości"
    assert bot.history[0]["role"] == "system", "Prompt systemowy musi zawsze zostać na pierwszym miejscu!"
    assert bot.history[-1]["content"] == "Odpowiedź 2", "Ostatnia wiadomość musi być zachowana"