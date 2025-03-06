"""
Interface de linha de comando para testar o chatbot.
"""

import os
import sys
from dotenv import load_dotenv

from src.memory import create_memory_store
from src.agent import create_chat_agent
from src.agent.chat_agent import chat


def main():
    """Função principal para a interface CLI."""
    # Carrega as variáveis de ambiente
    load_dotenv()
    
    # Verifica se a chave API está configurada
    if not os.getenv("OPENAI_API_KEY"):
        print("Erro: OPENAI_API_KEY não está configurada. Crie um arquivo .env com sua chave API.")
        sys.exit(1)
    
    # Cria o armazenamento de memória
    store = create_memory_store()
    
    # Cria o agente de chat
    agent = create_chat_agent(store=store)
    
    # Solicita o ID do usuário
    user_id = input("Digite seu ID de usuário (ou pressione Enter para usar 'default_user'): ").strip()
    if not user_id:
        user_id = "default_user"
    
    # Gera um ID de thread
    thread_id = f"thread_{user_id}"
    
    print(f"\nBem-vindo ao Chatbot com LangMem! (Usuário: {user_id}, Thread: {thread_id})")
    print("Digite 'sair' para encerrar a conversa.\n")
    
    # Loop de conversa
    while True:
        # Solicita a mensagem do usuário
        user_message = input("Você: ")
        
        # Verifica se o usuário quer sair
        if user_message.lower() in ["sair", "exit", "quit"]:
            print("\nAté logo!")
            break
        
        # Obtém a resposta do agente
        try:
            response = chat(
                agent=agent,
                message=user_message,
                user_id=user_id,
                thread_id=thread_id,
            )
            
            # Exibe a resposta
            print(f"\nAssistente: {response}\n")
        except Exception as e:
            print(f"\nErro: {str(e)}\n")


if __name__ == "__main__":
    main() 