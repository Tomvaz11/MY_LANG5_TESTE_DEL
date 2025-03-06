"""
Exemplo de uso de perfis de usuário com LangMem.

Este exemplo demonstra como criar, atualizar e usar perfis de usuário
para personalizar as respostas do chatbot.
"""

import os
from collections import defaultdict

from src.memory import (
    create_profile_manager, 
    update_user_profile,
    get_user_profile,
    UserProfile,
)


# Classe simulada de armazenamento
class MockStore:
    def __init__(self):
        self.profiles = {}
    
    def get(self, key, default=None):
        return self.profiles.get(key, default)
    
    def set(self, key, value):
        self.profiles[key] = value


# Classe simulada de agente
class MockAgent:
    def __init__(self, store):
        self.store = store
        self.responses = [
            "Olá, Maria! É um prazer conhecer uma desenvolvedora de software que aprecia música clássica e jazz. Como posso ajudar você hoje?",
            "Que projeto interessante, Maria! Combinar suas habilidades em Python e JavaScript para criar um aplicativo de recomendação de música é uma ótima ideia. Você está usando alguma API específica para obter os dados musicais?",
            "Para trabalhar com dados musicais em Python, recomendo algumas bibliotecas excelentes:\n\n1. Librosa - Ótima para análise de áudio e extração de características musicais\n2. Essentia - Uma ferramenta robusta para análise de áudio e música\n3. Music21 - Perfeita para análise de teoria musical e composição\n4. Pydub - Para manipulação simples de arquivos de áudio\n5. Spotipy - Wrapper Python para a API do Spotify, útil para obter metadados de música\n\nConsiderando seu interesse em jazz e música clássica, Music21 pode ser especialmente útil para análise de estruturas musicais mais complexas."
        ]
        self.response_index = 0
    
    def invoke(self, message, user_id=None, thread_id=None, user_profile=None):
        response = self.responses[self.response_index]
        self.response_index = min(self.response_index + 1, len(self.responses) - 1)
        return response


def main():
    """
    Função principal que demonstra o uso de perfis de usuário.
    """
    print("Exemplo de uso de perfis de usuário com LangMem\n")
    
    # Cria o armazenamento simulado
    store = MockStore()
    
    # Cria o agente simulado
    agent = MockAgent(store)
    
    # Cria o gerenciador de perfis
    profile_manager = create_profile_manager()
    
    # ID do usuário para este exemplo
    user_id = "exemplo_maria"
    
    # Simulação de uma conversa
    print("Iniciando conversa com o usuário...\n")
    
    # Primeira mensagem - apresentação
    primeira_mensagem = "Olá! Meu nome é Maria. Sou desenvolvedora de software e adoro música clássica e jazz."
    
    print(f"Usuário: {primeira_mensagem}")
    
    # Simulando uma resposta manual para o primeiro turno
    resposta = agent.invoke(primeira_mensagem, user_id=user_id)
    print(f"Assistente: {resposta}\n")
    
    # Atualiza o perfil com a primeira mensagem
    conversation_messages = [
        {"role": "user", "content": primeira_mensagem},
        {"role": "assistant", "content": resposta}
    ]
    update_user_profile(profile_manager, conversation_messages, user_id)
    
    # Armazena o perfil atualizado no store simulado
    key = f"profile/{user_id}"
    profile = UserProfile(
        name="Maria",
        interests=["música clássica", "jazz"],
        expertise_level="Desenvolvedora de software"
    )
    store.set(key, profile)
    
    # Verificação do perfil após a primeira mensagem
    perfil = get_user_profile(store, user_id)
    print("Perfil após a primeira mensagem:")
    print(f"Nome: {perfil.name if perfil and perfil.name else 'Não definido'}")
    print(f"Interesses: {', '.join(perfil.interests) if perfil and perfil.interests else 'Não definidos'}")
    print(f"Expertise: {perfil.expertise_level if perfil and perfil.expertise_level else 'Não definido'}\n")
    
    # Segunda mensagem - mais informações
    segunda_mensagem = "Estou trabalhando em um aplicativo de recomendação de música usando Python e JavaScript."
    
    print(f"Usuário: {segunda_mensagem}")
    resposta = agent.invoke(segunda_mensagem, user_id=user_id, user_profile=perfil)
    print(f"Assistente: {resposta}\n")
    
    # Atualiza o perfil com a segunda mensagem
    conversation_messages = [
        {"role": "user", "content": segunda_mensagem},
        {"role": "assistant", "content": resposta}
    ]
    update_user_profile(profile_manager, conversation_messages, user_id)
    
    # Atualiza o perfil no store simulado
    perfil.interests.extend(["Desenvolvimento de aplicativos", "Python", "JavaScript", "Recomendação musical"])
    store.set(key, perfil)
    
    # Verificação do perfil após a segunda mensagem
    perfil = get_user_profile(store, user_id)
    print("Perfil após a segunda mensagem:")
    print(f"Nome: {perfil.name if perfil and perfil.name else 'Não definido'}")
    print(f"Interesses: {', '.join(perfil.interests) if perfil and perfil.interests else 'Não definidos'}")
    print(f"Expertise: {perfil.expertise_level if perfil and perfil.expertise_level else 'Não definido'}\n")
    
    # Terceira mensagem - pergunta sobre interesse
    terceira_mensagem = "Você pode recomendar alguma biblioteca Python para trabalhar com dados musicais?"
    
    print(f"Usuário: {terceira_mensagem}")
    resposta = agent.invoke(terceira_mensagem, user_id=user_id, user_profile=perfil)
    print(f"Assistente: {resposta}\n")
    
    print("Exemplo concluído.")


if __name__ == "__main__":
    main() 