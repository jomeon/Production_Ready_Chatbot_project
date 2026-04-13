# Projekt APIS AI - Chatbot LLM (Llama 3)

## 1. Cel i zakres projektu
Celem projektu było zbudowanie produkcyjnej wersji chatbota opartego na modelu językowym (LLM). System został zaprojektowany tak, aby obsługiwać wielu użytkowników jednocześnie (sesje), zarządzać kontekstem rozmowy i działać w pełni lokalnie.

## 2. Architektura systemu
System opiera się na architekturze modularnej:
* **FastAPI:** Obsługuje warstwę sieciową i walidację danych (Pydantic).
* **SessionManager:** Izoluje rozmowy poszczególnych użytkowników w pamięci RAM.
* **APISChatbot (Core):** Klasa zarządzająca logiką, historią i oknem kontekstowym.
* **Ollama API:** Lokalny silnik uruchamiający model Llama 3.



## 3. Wybór modelu i integracja
* **Model:** Llama 3 (8B) via Ollama.
* **Uzasadnienie:** Wybór padł na rozwiązanie lokalne, aby wyeliminować koszty API i limity zapytań. Model 8B jest wystarczająco szybki do pracy na domowym sprzęcie, zachowując wysoką jakość odpowiedzi w języku polskim.
* **Technologie:** Python 3.10, FastAPI, Uvicorn, Ollama-python.

## 4. Inżynieria Promptów (Prompt Engineering)
Wykorzystano **Prompt Systemowy**, który definiuje tożsamość bota: 
> "Jesteś profesjonalnym i pomocnym asystentem AI. Odpowiadaj zwięźle, rzeczowo i zawsze w języku polskim."

Zapobiega to przełączaniu się modelu na język angielski i wymusza konkretny, techniczny ton wypowiedzi.

## 5. Historia i zarządzanie kontekstem (Wymóg 4.0)
Ponieważ modele LLM są bezstanowe, każdorazowo przesyłana jest cała historia konwersacji. 
* **Sliding Window:** Aby uniknąć przepełnienia pamięci, zaimplementowano mechanizm "przesuwnego okna". 
* **Ochrona Promptu:** Mechanizm usuwa najstarsze wiadomości, ale **zawsze zachowuje prompt systemowy** na początku listy, dzięki czemu bot nie traci instrukcji bazowych.

## 6. Parametry generowania
Zastosowano parametry optymalne dla naturalnej rozmowy:
* **Temperature (0.7):** Balans między przewidywalnością a kreatywnością.
* **Top_p (0.9):** Ograniczenie wyboru słów do tych najbardziej sensownych statystycznie.

## 7. Obsługa błędów i logi (Wymóg 4.5)
System jest odporny na błędy komunikacji (np. wyłączony silnik Ollama):
* Błędy są przechwytywane przez bloki `try-except`.
* W przypadku błędu historia jest automatycznie cofana o jeden krok, aby nie dopuścić do desynchronizacji.
* Wszystkie wyjątki trafiają do pliku `logs/chatbot_errors.log`.

## 8. Wdrożenie i REST API (Wymóg 5.0)
Chatbot jest udostępniony jako usługa REST. 
* **Endpointy:** `POST /chat` (rozmowa), `DELETE /chat/{id}` (reset sesji).
* **Dokumentacja:** Automatyczny Swagger UI dostępny pod `/docs`.
* **CI/CD:** Podpięte GitHub Actions, które przy każdym "pushu" sprawdza poprawność importów i uruchamia testy jednostkowe (`pytest`).

---
*Projekt przygotowany w ramach przedmiotu APIS AI.*