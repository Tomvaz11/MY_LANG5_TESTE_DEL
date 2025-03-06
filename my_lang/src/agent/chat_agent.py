"""
Agente de chat com LangMem.

Este módulo implementa um agente de chat que utiliza memória para lembrar de
informações importantes sobre o usuário e a conversa.
"""

import logging
import traceback
from typing import Dict, Any, Optional, List

# Importações corretas
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore

from langmem import create_manage_memory_tool, create_search_memory_tool

from src.config import (
    MODEL_NAME,
    SYSTEM_INSTRUCTIONS,
    MEMORY_NAMESPACE,
    MEMORY_INSTRUCTIONS,
    SEARCH_INSTRUCTIONS,
)
from src.memory import (
    create_memory_store,
    create_background_memory_manager,
    schedule_memory_processing,
    create_profile_manager,
    get_user_profile,
    update_user_profile,
    create_memory_prompt_function,
)

# Configurar logger
logger = logging.getLogger(__name__)


def create_chat_agent(
    store: Optional[InMemoryStore] = None,
    system_instructions: str = SYSTEM_INSTRUCTIONS,
    model_name: str = MODEL_NAME,
    enable_background_memory: bool = True,
    enable_user_profiles: bool = True,
) -> Dict:
    """
    Cria um agente de chat com LangMem.
    
    Args:
        store (InMemoryStore): Armazenamento para memórias
        system_instructions (str): Instruções do sistema
        model_name (str): Nome do modelo a ser usado
        enable_background_memory (bool): Se deve habilitar memória em segundo plano
        enable_user_profiles (bool): Se deve habilitar perfis de usuário
        
    Returns:
        Dict: Componentes do agente (agent, background_memory_manager, profile_manager)
    """
    logger.info(f"Criando agente de chat com modelo {model_name}")
    
    # Cria o armazenamento se não for fornecido
    if store is None:
        logger.info("Criando armazenamento de memória")
        store = create_memory_store()
    
    # Configuramos o checkpointer para manter o estado das conversas
    checkpointer = InMemorySaver()
    
    # Configura as ferramentas de memória
    logger.info("Configurando ferramentas de memória")
    memory_tools = [
        create_manage_memory_tool(
            namespace=MEMORY_NAMESPACE,
            instructions=MEMORY_INSTRUCTIONS
        ),
        create_search_memory_tool(
            namespace=MEMORY_NAMESPACE,
            instructions=SEARCH_INSTRUCTIONS
        )
    ]
    
    # Obtém a função de prompt que adiciona memórias relevantes
    memory_prompt_fn = create_memory_prompt_function()

    # Criamos o modelo LLM
    logger.info(f"Inicializando modelo {model_name}")
    model = ChatOpenAI(model=model_name)
    
    # Cria o agente LangGraph com suporte a ferramentas de memória LangMem
    logger.info("Criando agente ReAct com ferramentas de memória")
    agent = create_react_agent(
        model,
        tools=memory_tools,
        prompt=memory_prompt_fn,
        store=store,
        checkpointer=checkpointer,
    )
    
    # Cria o gerenciador de memória em segundo plano se habilitado
    background_memory_manager = None
    if enable_background_memory:
        logger.info("Criando gerenciador de memória em segundo plano")
        background_memory_manager = create_background_memory_manager(store=store)
    
    # Cria o gerenciador de perfis se habilitado
    profile_manager = None
    if enable_user_profiles:
        logger.info("Criando gerenciador de perfis de usuário")
        profile_manager = create_profile_manager(model_name=model_name)
    
    logger.info("Agente de chat criado com sucesso")
    return {
        "agent": agent,
        "background_memory_manager": background_memory_manager,
        "profile_manager": profile_manager
    }


def chat(
    agent: Any, 
    message: str, 
    user_id: str = "default_user", 
    thread_id: str = "default_thread",
    background_memory_manager = None,
    profile_manager = None,
) -> str:
    """
    Função para enviar uma mensagem ao agente e obter a resposta.
    
    Args:
        agent (Any): O agente de chat
        message (str): Mensagem do usuário
        user_id (str): ID do usuário
        thread_id (str): ID da conversa
        background_memory_manager: Gerenciador de memória em segundo plano
        profile_manager: Gerenciador de perfis de usuário
        
    Returns:
        str: Resposta do agente
    """
    logger.info(f"Processando chat. Usuário: {user_id}, Thread: {thread_id}")
    
    # Invocar o agente com a mensagem
    try:
        logger.debug("Invocando agente")
        response = agent.invoke(
            {"messages": [{"role": "user", "content": message}]},
            config={"configurable": {"user_id": user_id, "thread_id": thread_id}}
        )
        
        # Extrai a resposta do agente - garantindo que seja uma string
        agent_response = ""
        try:
            # Tenta extrair a resposta do formato retornado
            if isinstance(response, dict) and "messages" in response:
                last_message = response["messages"][-1]
                if isinstance(last_message, dict) and "content" in last_message:
                    agent_response = last_message["content"]
                elif hasattr(last_message, "content"):
                    agent_response = last_message.content
            elif hasattr(response, "messages"):
                messages = response.messages
                if hasattr(messages[-1], "content"):
                    agent_response = messages[-1].content
            elif isinstance(response, str):
                agent_response = response
            else:
                logger.error(f"Formato de resposta desconhecido: {type(response)}")
                agent_response = "Desculpe, não foi possível processar sua mensagem."
        except (KeyError, AttributeError, IndexError) as e:
            logger.error(f"Erro ao extrair resposta: {str(e)}")
            logger.error(traceback.format_exc())
            agent_response = "Desculpe, ocorreu um erro ao processar sua mensagem."
        
        # Estrutura a conversa
        user_message = {"role": "user", "content": message}
        assistant_message = {"role": "assistant", "content": agent_response}
        conversation_messages = [user_message, assistant_message]
        
        # Atualiza o perfil do usuário se o gerenciador estiver disponível
        if profile_manager is not None:
            try:
                logger.debug(f"Atualizando perfil do usuário {user_id}")
                update_user_profile(profile_manager, conversation_messages, user_id)
            except Exception as e:
                logger.error(f"Erro ao atualizar perfil do usuário: {str(e)}")
                logger.error(traceback.format_exc())
        
        # Agenda o processamento de memória em segundo plano
        if background_memory_manager is not None:
            try:
                logger.debug(f"Agendando processamento de memória para usuário {user_id}")
                schedule_memory_processing(
                    background_memory_manager,
                    conversation_messages,
                    user_id=user_id
                )
            except Exception as e:
                logger.error(f"Erro ao agendar processamento de memória: {str(e)}")
                logger.error(traceback.format_exc())
        
        return agent_response
    except Exception as e:
        logger.error(f"Erro ao processar chat: {str(e)}")
        logger.error(traceback.format_exc())
        return f"Desculpe, ocorreu um erro ao processar sua mensagem. Detalhes: {str(e)}"