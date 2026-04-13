# APIS AI - Projekt Chatbot 

Produkcyjna wersja chatbota LLM zrealizowana w ramach projektu APIS.
Wykorzystuje lokalny model **Llama 3** (via Ollama) i udostępnia go przez wysokowydajne REST API (FastAPI) z obsługą wielu sesji równolegle.

## Wymagania
* Python 3.10+
* Conda / Mamba
* Zainstalowany silnik [Ollama](https://ollama.com/) z pobranym modelem `llama3`.

## Uruchomienie
1. `conda env create -f environment.yml`
2. `conda activate apis_chatbot`
3. `uvicorn app.main:app --reload`
4. Przejdź pod `http://127.0.0.1:8000/docs`, aby testować API w Swagger UI.