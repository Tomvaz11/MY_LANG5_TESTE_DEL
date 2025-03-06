"""
Processamento de memória em segundo plano (Background Formation) usando LangMem.
"""

from typing import Dict, Any, Optional
import logging
import traceback
from concurrent.futures import CancelledError

from langmem import ReflectionExecutor, create_memory_store_manager
from langgraph.store.memory import InMemoryStore
from langgraph.config import RunnableConfig

from src.config import (
    MEMORY_NAMESPACE,
    MODEL_NAME,
    EMBEDDING_MODEL,
)

# Configuração de logging
logger = logging.getLogger("memory_background")
logger.setLevel(logging.DEBUG)


def create_background_memory_manager(
    store: Optional[InMemoryStore] = None,
    model_name: str = MODEL_NAME,
    namespace: tuple = MEMORY_NAMESPACE,
    query_limit: int = 5,
) -> ReflectionExecutor:
    """
    Cria um gerenciador de memória em segundo plano usando ReflectionExecutor.
    
    O processamento em segundo plano permite extrair e consolidar memórias sem
    adicionar latência às respostas do chatbot. Isso é ideal para análise de padrões
    e extração de insights após as conversas.
    
    Args:
        store (Optional[InMemoryStore]): O armazenamento para memórias
        model_name (str): Nome do modelo de linguagem
        namespace (tuple): Namespace para armazenamento das memórias
        query_limit (int): Número máximo de memórias relevantes a serem recuperadas
        
    Returns:
        ReflectionExecutor: Executor para processamento de memória em segundo plano
    """
    logger.info(f"Criando gerenciador de memória em segundo plano com modelo {model_name}")
    
    # Criamos o gerenciador de memória
    memory_manager = create_memory_store_manager(
        model_name,  # Passamos como argumento posicional, não como keyword
        namespace=namespace,
        query_limit=query_limit,
    )
    
    # Envolvemos o gerenciador em um ReflectionExecutor para processamento em segundo plano
    executor = ReflectionExecutor(memory_manager, store=store)
    
    logger.info("Gerenciador de memória em segundo plano criado com sucesso")
    
    return executor


def schedule_memory_processing(
    executor: ReflectionExecutor,
    messages: list,
    user_id: str = "default_user",
    delay_seconds: float = 30.0,
) -> None:
    """
    Agenda o processamento de memória em segundo plano com um atraso específico.
    
    O atraso permite acumular mais contexto antes de processar as memórias, evitando
    trabalho redundante em conversas ativas.
    
    Args:
        executor (ReflectionExecutor): Executor para processamento em segundo plano
        messages (list): Lista de mensagens da conversa
        user_id (str): ID do usuário
        delay_seconds (float): Atraso em segundos antes do processamento
    """
    try:
        logger.info(f"Agendando processamento de memória para o usuário {user_id} com atraso de {delay_seconds}s")
        
        # Formatamos as mensagens no formato compatível
        to_process = {
            "messages": messages,
        }
        
        # Criamos uma configuração explícita
        config = RunnableConfig(
            configurable={
                "user_id": user_id,
            }
        )
        
        # Agendamos o processamento com o atraso especificado e a configuração
        future = executor.submit(to_process, after_seconds=delay_seconds, config=config)
        
        # Adicionamos callback para monitorar o status da tarefa
        def done_callback(future):
            try:
                if future.cancelled():
                    logger.info(f"Processamento de memória cancelado para o usuário {user_id}")
                else:
                    result = future.result()
                    logger.info(f"Processamento de memória concluído para o usuário {user_id}")
            except CancelledError:
                logger.info(f"Processamento de memória cancelado para o usuário {user_id}")
            except Exception as e:
                logger.error(f"Erro no processamento de memória: {str(e)}")
                logger.error(traceback.format_exc())
        
        future.add_done_callback(done_callback)
        
    except Exception as e:
        logger.error(f"Erro ao agendar processamento de memória: {str(e)}")
        logger.error(traceback.format_exc()) 