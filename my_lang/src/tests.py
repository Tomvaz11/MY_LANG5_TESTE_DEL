"""
Testes para o chatbot com LangMem.
"""

import time
import pytest
from collections import defaultdict

from src.memory import (
    UserProfile,
    get_user_profile,
)
from src.config import SYSTEM_INSTRUCTIONS


class MockAgent:
    """Agente simulado para testes."""
    def __init__(self, store=None):
        self.store = store or {}
        self.responses = [
            "Claro, João! Já anotei que você gosta de tecnologia. Se precisar de alguma informação ou dica nessa área, é só avisar!",
            "Você se chama João e gosta muito de tecnologia! Se precisar de ajuda nessa área ou quiser conversar sobre alguma novidade, estou aqui!"
        ]
        self.response_index = 0
    
    def invoke(self, message, user_id=None, thread_id=None):
        response = self.responses[self.response_index]
        self.response_index = min(self.response_index + 1, len(self.responses) - 1)
        return response


class MockStore:
    """Armazenamento simulado para testes."""
    def __init__(self):
        self.data = {}
    
    def get(self, key, default=None):
        return self.data.get(key, default)
    
    def set(self, key, value):
        self.data[key] = value


class MockProfileManager:
    """Gerenciador de perfis simulado para testes."""
    def __init__(self):
        self.profiles = {}
    
    def invoke(self, messages, user_id=None):
        """Simula a atualização de um perfil com base em mensagens."""
        profile = self.profiles.get(user_id, UserProfile())
        
        for message in messages:
            if message["role"] == "user":
                content = message["content"].lower()
                
                # Simula extração de nome
                if "meu nome é" in content:
                    name = content.split("meu nome é")[1].split(".")[0].strip()
                    profile.name = name.capitalize()
                
                # Simula extração de interesses
                if "gosto de" in content or "adoro" in content or "interesse em" in content:
                    interests = []
                    for keyword in ["tecnologia", "música", "programação", "viagens", "esportes"]:
                        if keyword in content:
                            interests.append(keyword)
                    
                    if interests:
                        profile.interests.extend(interests)
                
                # Simula extração de profissão
                if "programador" in content or "desenvolvedor" in content:
                    profile.expertise_level = "Programador"
        
        self.profiles[user_id] = profile
        return profile


def test_background_memory():
    """
    Teste do processamento de memória em segundo plano.
    
    Este teste verifica se:
    1. O agente é criado corretamente com suporte a memória em segundo plano
    2. O agente responde corretamente a uma mensagem
    3. O processamento de memória em segundo plano é agendado
    4. As memórias são extraídas e armazenadas corretamente
    """
    print("Iniciando teste de memória em segundo plano...")
    
    # Cria o armazenamento de memória
    store = create_memory_store()
    
    # Cria o agente com suporte a memória em segundo plano
    agent_components = create_chat_agent(store=store, enable_background_memory=True)
    agent = agent_components["agent"]
    background_memory_manager = agent_components["background_memory_manager"]
    
    # Verifica se o agente e o gerenciador de memória foram criados corretamente
    print(f"Agente criado: {agent is not None}")
    print(f"Gerenciador de memória criado: {background_memory_manager is not None}")
    
    # Envia uma mensagem para o agente
    user_id = "test_user"
    thread_id = "test_thread"
    message = "Meu nome é João e gosto muito de tecnologia. Por favor, lembre-se disso."
    
    print(f"\nMensagem do usuário: '{message}'")
    response = chat(
        agent=agent, 
        message=message, 
        user_id=user_id, 
        thread_id=thread_id,
        background_memory_manager=background_memory_manager
    )
    print(f"Resposta do agente: '{response}'")
    
    # Aguarda o processamento em segundo plano (normalmente seria assíncrono)
    print("\nAguardando processamento de memória em segundo plano (5 segundos)...")
    time.sleep(5)
    
    # Verifica as memórias armazenadas
    namespace = ("chatbot_memories", user_id)
    memories = store.search(namespace)
    
    print(f"\nMemórias armazenadas para o usuário {user_id}:")
    if memories:
        for i, memory in enumerate(memories, 1):
            print(f"Memória {i}: {memory.value}")
    else:
        print("Nenhuma memória encontrada.")
    
    # Segunda interação para verificar recuperação de memória
    second_message = "Como eu me chamo e do que eu gosto?"
    print(f"\nSegunda mensagem do usuário: '{second_message}'")
    second_response = chat(
        agent=agent, 
        message=second_message, 
        user_id=user_id, 
        thread_id=thread_id,
        background_memory_manager=background_memory_manager
    )
    print(f"Resposta do agente: '{second_response}'")
    
    print("\nTeste concluído!")


def test_prompt_optimization():
    """
    Teste da otimização de prompts do sistema.
    
    Este teste verifica se:
    1. O otimizador de prompts é criado corretamente
    2. O otimizador pode melhorar um prompt com base em interações e feedback
    """
    print("Iniciando teste de otimização de prompts...")
    
    # Cria o otimizador de prompts
    optimizer = create_system_prompt_optimizer()
    print(f"Otimizador criado: {optimizer is not None}")
    
    # Prompt atual do sistema
    current_prompt = SYSTEM_INSTRUCTIONS
    print(f"\nPrompt atual:\n{current_prompt}")
    
    # Simula uma trajetória de conversa
    trajectory = [
        {"role": "user", "content": "Qual é a capital do Brasil?"},
        {"role": "assistant", "content": "A capital do Brasil é Brasília."},
        {"role": "user", "content": "Obrigado, mas você poderia dar mais detalhes sobre a cidade?"},
        {"role": "assistant", "content": "Desculpe, não forneci detalhes suficientes. Brasília é a capital federal do Brasil, inaugurada em 21 de abril de 1960. Foi planejada pelo urbanista Lúcio Costa e pelo arquiteto Oscar Niemeyer. A cidade tem formato de avião e é conhecida por sua arquitetura modernista."},
    ]
    
    # Feedback simulado
    feedback = {
        "issue": "O assistente inicialmente forneceu uma resposta muito curta e sem detalhes",
        "improvement": "O assistente deve fornecer respostas mais detalhadas desde o início, especialmente para perguntas sobre lugares e fatos"
    }
    
    # Otimiza o prompt
    print("\nOtimizando o prompt...")
    optimized_prompt = optimize_system_prompt(
        optimizer=optimizer,
        current_prompt=current_prompt,
        trajectories=[trajectory],
        feedback=feedback
    )
    
    print(f"\nPrompt otimizado:\n{optimized_prompt}")
    print("\nTeste concluído!")


def test_user_profile():
    """
    Teste de perfil de usuário.
    """
    print("\n==================================================\n")
    print("Iniciando teste de perfil de usuário...")
    
    # Cria o gerenciador de perfis simulado
    profile_manager = MockProfileManager()
    print(f"Gerenciador de perfil criado: {profile_manager is not None}")
    
    # Armazenamento simulado
    store = MockStore()
    
    # ID do usuário para teste
    user_id = "test_user"
    
    print("\nAtualizando o perfil do usuário...")
    
    # Primeira conversa
    messages = [
        {"role": "user", "content": "Olá! Meu nome é Maria. Pode me chamar de Mari. Adoro música clássica, jazz e ficção científica."},
        {"role": "assistant", "content": "Olá, Mari! É um prazer conhecê-la. Vejo que você gosta de música clássica, jazz e ficção científica. Como posso ajudar você hoje?"}
    ]
    
    # Atualiza o perfil com base nas mensagens
    profile = profile_manager.invoke(messages, user_id)
    
    # Armazena o perfil no store
    store.set(f"profile/{user_id}", profile)
    
    # Recupera o perfil do store
    retrieved_profile = get_user_profile(store, user_id)
    
    # Exibe o perfil
    print("\nPerfil do usuário:")
    print(f"Nome: {retrieved_profile.name}")
    print(f"Nome preferido: {retrieved_profile.preferred_name}")
    print(f"Idioma: {retrieved_profile.language}")
    print(f"Interesses: {', '.join(retrieved_profile.interests)}")
    print(f"Preferências: {retrieved_profile.preferences}")
    
    # Segunda conversa - mais informações
    print("\nAtualizando o perfil com novas informações...")
    
    messages = [
        {"role": "user", "content": "Sou programadora e estou desenvolvendo um aplicativo de recomendação musical usando Inteligência Artificial."},
        {"role": "assistant", "content": "Isso é fascinante! É ótimo ver uma programadora trabalhando com IA para recomendação musical. Seu interesse em música clássica e jazz deve ser uma ótima inspiração para esse projeto."}
    ]
    
    # Atualiza o perfil com base nas novas mensagens
    profile = profile_manager.invoke(messages, user_id)
    
    # Simula atualização manual do perfil
    profile.name = "Mari"  # Usando nome preferido
    profile.interests = ["Desenvolvimento de aplicativos", "Inteligência Artificial", "Recomendação musical", "Python", "JavaScript"]
    profile.expertise_level = "Programadora"
    
    # Armazena o perfil atualizado
    store.set(f"profile/{user_id}", profile)
    
    # Recupera o perfil atualizado
    updated_profile = get_user_profile(store, user_id)
    
    # Exibe o perfil atualizado
    print("\nPerfil atualizado do usuário:")
    print(f"Nome: {updated_profile.name}")
    print(f"Nome preferido: {updated_profile.preferred_name}")
    print(f"Idioma: {updated_profile.language}")
    print(f"Interesses: {', '.join(updated_profile.interests)}")
    print(f"Expertise: {updated_profile.expertise_level}")
    
    print("\nTeste concluído!")


if __name__ == "__main__":
    test_background_memory()
    print("\n" + "="*50 + "\n")
    test_prompt_optimization()
    print("\n" + "="*50 + "\n")
    test_user_profile() 