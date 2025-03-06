"""
Aplicação principal do chatbot com LangMem.
"""

import os
import sys
import logging
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# Adiciona o diretório raiz ao path do Python
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from src.config import API_HOST, API_PORT
from src.memory import create_memory_store
from src.agent import create_chat_agent
from src.api import create_api

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("chatbot.log")
    ]
)
logger = logging.getLogger(__name__)


def main():
    """
    Função principal que inicia o chatbot.
    """
    try:
        logger.info("Iniciando chatbot com LangMem")
        
        # Cria o armazenamento compartilhado para memórias
        logger.info("Criando armazenamento de memória")
        store = create_memory_store()
        
        # Cria o agente de chat
        logger.info("Criando agente de chat com gerenciador de memória")
        agent_components = create_chat_agent(
            store=store, 
            enable_background_memory=True,
            enable_user_profiles=True
        )
        agent = agent_components["agent"]
        background_memory_manager = agent_components["background_memory_manager"]
        profile_manager = agent_components["profile_manager"]
        
        # Cria a API
        logger.info("Criando API")
        app = create_api(
            agent=agent, 
            background_memory_manager=background_memory_manager,
            profile_manager=profile_manager
        )
        
        # Adiciona middleware CORS
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Em produção, restrinja para origens específicas
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Inicia o servidor
        logger.info(f"Iniciando servidor na porta {API_PORT}...")
        print(f"Iniciando servidor na porta {API_PORT}...")
        uvicorn.run(app, host=API_HOST, port=API_PORT)
    except Exception as e:
        logger.error(f"Erro ao iniciar o chatbot: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    main() 