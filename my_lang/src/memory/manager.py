"""
Gerenciamento de memória para o chatbot usando LangMem.
"""

from typing import Callable, Dict, List, Tuple, Any
import asyncio

from langmem import create_manage_memory_tool, create_search_memory_tool
from langgraph.store.memory import InMemoryStore
from langgraph.store.postgres import AsyncPostgresStore, PoolConfig
from langgraph.config import get_store

from src.config import (
    MEMORY_NAMESPACE,
    MEMORY_INSTRUCTIONS,
    SEARCH_INSTRUCTIONS,
    EMBEDDING_MODEL,
    USE_POSTGRES,
    POSTGRES_CONNECTION_STRING,
    POSTGRES_POOL_MIN_SIZE,
    POSTGRES_POOL_MAX_SIZE,
)


def create_memory_store():
    """
    Cria o armazenamento de memória usando PostgreSQL ou InMemoryStore.
    
    Returns:
        Store: O objeto de armazenamento para memórias (AsyncPostgresStore ou InMemoryStore)
    """
    # Configuração comum para embeddings
    index_config = {
        "dims": 1536,  # Dimensionalidade dos embeddings
        "embed": EMBEDDING_MODEL,  # Modelo para embeddings
    }

    if USE_POSTGRES:
        # Configuração para PostgreSQL com pgvector
        async def setup_postgres_store():
            # Configuração do pool de conexões
            pool_config = PoolConfig(
                min_size=POSTGRES_POOL_MIN_SIZE,
                max_size=POSTGRES_POOL_MAX_SIZE
            )
            
            # Criação do store com pool de conexões
            store = None
            async with AsyncPostgresStore.from_conn_string(
                POSTGRES_CONNECTION_STRING,
                pool_config=pool_config,
                index=index_config
            ) as async_store:
                # Executa a configuração inicial (migrações)
                await async_store.setup()
                store = async_store
                
                # Retorna o store configurado
                return store
                
        # Executa a configuração de forma síncrona
        return asyncio.run(setup_postgres_store())
    else:
        # Usa o InMemoryStore padrão quando PostgreSQL não está habilitado
        return InMemoryStore(index=index_config)


def create_memory_tools(namespace: Tuple[str, ...] = MEMORY_NAMESPACE) -> List[Callable]:
    """
    Cria as ferramentas de memória para o agente.
    
    Args:
        namespace (Tuple[str, ...]): Namespace para armazenamento das memórias
        
    Returns:
        List[Callable]: Lista de ferramentas de memória
    """
    return [
        create_manage_memory_tool(
            namespace=namespace,
            instructions=MEMORY_INSTRUCTIONS,
        ),
        create_search_memory_tool(
            namespace=namespace,
            instructions=SEARCH_INSTRUCTIONS,
        ),
    ]


def create_memory_prompt_function() -> Callable:
    """
    Cria uma função de prompt que recupera memórias relevantes.
    
    Returns:
        Callable: Função de prompt que adiciona memórias relevantes
    """
    
    def prompt_with_memories(state: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Função de prompt que adiciona memórias relevantes ao início da conversa.
        
        Args:
            state (Dict[str, Any]): Estado atual da conversa
            
        Returns:
            List[Dict[str, str]]: Lista de mensagens incluindo memórias relevantes
        """
        # Obtém o armazenamento
        store = get_store()
        
        # Se não há mensagens, retorna apenas a mensagem do sistema
        if not state.get("messages"):
            return state.get("messages", [])
        
        # Obtém a última mensagem do usuário para buscar memórias relevantes
        if isinstance(state["messages"][-1], dict):
            last_message = state["messages"][-1].get("content", "")
        else:
            last_message = getattr(state["messages"][-1], "content", "")
        
        # Configuráveis para o namespace
        configurable = state.get("configurable", {})
        user_id = configurable.get("user_id", "default_user")
        
        # Resolve o namespace com o ID do usuário
        namespace = tuple(
            part.format(user_id=user_id) if isinstance(part, str) else part
            for part in MEMORY_NAMESPACE
        )
        
        # Busca memórias relevantes
        try:
            items = store.search(namespace, query=last_message, limit=5)
            if items:
                memories = "\n\n".join(f"- {item.value}" for item in items)
                
                # Cria a mensagem de sistema com memórias
                system_msg = {
                    "role": "system", 
                    "content": f"## Memórias Relevantes:\n\n{memories}\n\nUse estas informações quando relevante, mas não mencione explicitamente que está usando 'memórias'."
                }
                
                # Adiciona a mensagem de sistema no início das mensagens
                return [system_msg] + state["messages"]
        except Exception:
            # Se houver erro, apenas retorna as mensagens originais
            pass
            
        return state["messages"]
    
    return prompt_with_memories 