"""
Gerenciamento de perfis de usuário usando LangMem.

Este módulo implementa funcionalidades para criar, atualizar e recuperar perfis de usuário,
que são representações estruturadas de informações sobre os usuários.
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel

from langmem import create_memory_manager, create_memory_store_manager
from langgraph.store.memory import InMemoryStore

from src.config import MODEL_NAME, MEMORY_NAMESPACE


class UserProfile(BaseModel):
    """
    Modelo para o perfil do usuário.
    
    Armazena informações estruturadas sobre o usuário, como nome, preferências,
    interesses e outras informações relevantes.
    """
    name: Optional[str] = None
    preferred_name: Optional[str] = None
    language: Optional[str] = None
    timezone: Optional[str] = None
    interests: List[str] = []
    preferences: Dict[str, str] = {}
    communication_style: Optional[str] = None
    expertise_level: Optional[str] = None
    last_interaction: Optional[str] = None


def create_profile_manager(
    model_name: str = MODEL_NAME,
    namespace: tuple = MEMORY_NAMESPACE,
):
    """
    Cria um gerenciador de perfis de usuário.
    
    O gerenciador de perfis é responsável por extrair e atualizar informações
    de perfil a partir das conversas.
    
    Args:
        model_name (str): Nome do modelo de linguagem
        namespace (tuple): Namespace para armazenamento dos perfis
        
    Returns:
        callable: Gerenciador de perfis de usuário
    """
    # Instruções específicas para extração de perfil
    profile_instructions = """
    Extraia e atualize informações de perfil do usuário a partir da conversa.
    Foque em:
    
    1. Nome e nome preferido do usuário
    2. Idioma e fuso horário
    3. Interesses e hobbies
    4. Preferências de comunicação e estilo
    5. Nível de expertise em diferentes áreas
    
    Atualize apenas os campos para os quais você tem informações confiáveis.
    Mantenha os valores existentes para campos que não são mencionados na conversa atual.
    """
    
    # Criamos o gerenciador de perfis
    profile_manager = create_memory_manager(
        model_name,
        schemas=[UserProfile],
        instructions=profile_instructions,
        enable_inserts=False,  # Apenas atualiza o perfil existente, não cria novos
    )
    
    return profile_manager


def create_profile_store_manager(
    store: Optional[InMemoryStore] = None,
    model_name: str = MODEL_NAME,
):
    """
    Cria um gerenciador de perfis com armazenamento.
    
    Este gerenciador integra-se com o armazenamento do LangGraph para persistir
    os perfis de usuário.
    
    Args:
        store (Optional[InMemoryStore]): Armazenamento para perfis
        model_name (str): Nome do modelo de linguagem
        
    Returns:
        callable: Gerenciador de perfis com armazenamento
    """
    # Namespace específico para perfis
    profile_namespace = ("user_profiles", "{user_id}")
    
    # Instruções específicas para extração de perfil
    profile_instructions = """
    Extraia e atualize informações de perfil do usuário a partir da conversa.
    Foque em:
    
    1. Nome e nome preferido do usuário
    2. Idioma e fuso horário
    3. Interesses e hobbies
    4. Preferências de comunicação e estilo
    5. Nível de expertise em diferentes áreas
    
    Atualize apenas os campos para os quais você tem informações confiáveis.
    Mantenha os valores existentes para campos que não são mencionados na conversa atual.
    """
    
    # Criamos o gerenciador de perfis com armazenamento
    profile_store_manager = create_memory_store_manager(
        model_name,
        schemas=[UserProfile],
        instructions=profile_instructions,
        enable_inserts=False,  # Apenas atualiza o perfil existente, não cria novos
        namespace=profile_namespace,
        store=store,
    )
    
    return profile_store_manager


def get_user_profile(
    store: Any,
    user_id: str = "default_user",
) -> Optional[UserProfile]:
    """
    Recupera o perfil do usuário do armazenamento.
    
    Args:
        store: Armazenamento (InMemoryStore ou compatível)
        user_id (str): ID do usuário
        
    Returns:
        Optional[UserProfile]: Perfil do usuário ou None se não existir
    """
    profile_key = f"profile/{user_id}"
    
    # Verifica se o armazenamento é um dicionário ou tem método get
    if hasattr(store, "get"):
        # Tenta usar o método get
        profile_data = store.get(profile_key)
        if profile_data:
            # Se o perfil já for um objeto UserProfile, retorna-o diretamente
            if isinstance(profile_data, UserProfile):
                return profile_data
            # Caso contrário, converte para UserProfile
            return UserProfile(**profile_data)
    
    # Caso o armazenamento tenha método search (como o InMemoryStore do LangMem)
    elif hasattr(store, "search"):
        # Constrói o namespace para o perfil do usuário
        profile_namespace = f"profile/{user_id}"
        
        try:
            # Busca o perfil no armazenamento
            results = store.search(profile_namespace)
            
            # Se encontrou resultados, retorna o primeiro
            if results and len(results) > 0:
                profile_data = results[0].get("content", {})
                if profile_data:
                    return UserProfile(**profile_data)
        except Exception as e:
            print(f"Erro ao recuperar perfil do usuário: {e}")
    
    # Se não encontrou ou houve erro, retorna None
    return None


def update_user_profile(
    profile_manager,
    messages: List[Dict[str, Any]],
    user_id: str = "default_user",
) -> Optional[UserProfile]:
    """
    Atualiza o perfil de um usuário com base em novas mensagens.
    
    Args:
        profile_manager: Gerenciador de perfis
        messages (List[Dict[str, Any]]): Mensagens da conversa
        user_id (str): ID do usuário
        
    Returns:
        Optional[UserProfile]: Perfil atualizado do usuário
    """
    # Formata as mensagens para o gerenciador de perfis
    to_process = {
        "messages": messages,
        "configurable": {
            "user_id": user_id,
        }
    }
    
    # Invoca o gerenciador de perfis
    result = profile_manager.invoke(to_process)
    
    if result and len(result) > 0:
        return result[0].content
    
    return None 