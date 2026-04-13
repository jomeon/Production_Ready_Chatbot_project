from app.chatbot_core import APISChatbot

def run_test():
    print("Inicjalizacja chatbota... (Łączenie z lokalnym modelem Llama 3)")
    # Tworzymy instancję naszego bota
    bot = APISChatbot(model_name="llama3")
    print("-" * 50)
    print("Chatbot gotowy! Wpisz 'wyjdz', aby zakończyć.\n")

    while True:
        user_input = input("Ty: ")
        
        if user_input.lower() in ['wyjdz', 'exit', 'quit', 'q']:
            print("Zakończono testy.")
            break

        # Odpytujemy model
        response = bot.generate_response(user_input)
        print(f"APIS Bot: {response}\n")

if __name__ == "__main__":
    run_test()