"""
Rotas da API para o chatbot.
"""

import os
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
import uuid
import traceback

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from src.agent.chat_agent import chat

# Configurar logger
logger = logging.getLogger(__name__)


class ChatMessage(BaseModel):
    """Modelo para mensagens de chat."""
    role: str = Field(..., description="Papel do remetente (user ou assistant)")
    content: str = Field(..., description="Conteúdo da mensagem")


class ChatRequest(BaseModel):
    """Modelo para requisições de chat."""
    message: str = Field(..., description="Mensagem do usuário")
    user_id: str = Field("default_user", description="ID do usuário")
    thread_id: Optional[str] = Field(None, description="ID da conversa")


class ChatResponse(BaseModel):
    """Modelo para respostas de chat."""
    response: str = Field(..., description="Resposta do assistente")
    user_id: str = Field(..., description="ID do usuário")
    thread_id: str = Field(..., description="ID da conversa")


def create_api(agent: Any, background_memory_manager=None, profile_manager=None) -> FastAPI:
    """
    Cria a API do chatbot.
    
    Args:
        agent (Any): O agente de chat (pode ser MessageGraph ou outro objeto)
        background_memory_manager: Gerenciador de memória em segundo plano
        profile_manager: Gerenciador de perfis de usuário
        
    Returns:
        FastAPI: Aplicação FastAPI
    """
    logger.info("Inicializando API do chatbot")
    
    app = FastAPI(
        title="Chatbot com LangMem",
        description="API para um chatbot com memória de longo prazo usando LangMem",
        version="1.0.0",
    )
    
    # Diretório para arquivos estáticos da interface web
    static_dir = Path(__file__).parent / "static"
    static_dir.mkdir(exist_ok=True)
    
    # Monta os arquivos estáticos
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    
    @app.post("/chat", response_model=ChatResponse)
    async def chat_endpoint(request: ChatRequest) -> Dict:
        """
        Endpoint para receber mensagens do usuário e obter respostas do chatbot.
        
        Args:
            request (ChatRequest): Requisição de chat
            
        Returns:
            Dict: Resposta do chatbot
        """
        try:
            # Usa o thread_id da requisição ou gera um novo
            thread_id = request.thread_id or str(uuid.uuid4())
            
            logger.info(f"Processando mensagem. Usuário: {request.user_id}, Thread: {thread_id}, Mensagem: {request.message[:30]}...")
            print(f"Processando mensagem de {request.user_id} no thread {thread_id}: {request.message}")
            
            # Processa a mensagem com o agente de chat
            logger.debug("Enviando mensagem para o agente")
            response = chat(
                agent=agent,
                message=request.message,
                user_id=request.user_id,
                thread_id=thread_id,
                background_memory_manager=background_memory_manager,
                profile_manager=profile_manager,
            )
            
            logger.info(f"Resposta gerada para {request.user_id}: {response[:30]}...")
            print(f"Resposta gerada: {response}")
            
            # A função chat agora garante que a resposta seja uma string
            return {
                "response": response,
                "user_id": request.user_id,
                "thread_id": thread_id,
            }
        except Exception as e:
            # Captura e loga a exceção de forma detalhada
            error_msg = f"Erro no endpoint /chat: {str(e)}"
            error_trace = traceback.format_exc()
            logger.error(error_msg)
            logger.error(error_trace)
            print(error_msg)
            print(error_trace)
            
            # Retorna um erro HTTP 500 com detalhe útil
            raise HTTPException(
                status_code=500, 
                detail=f"Erro interno do servidor: {str(e)}. Verifique os logs para mais detalhes."
            )
    
    @app.get("/")
    async def root():
        """Rota raiz da API que serve a interface web."""
        logger.debug("Acessando página principal")
        return FileResponse(static_dir / "index.html")
    
    # Handler para erros não tratados
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        logger.error(f"Erro não tratado: {str(exc)}")
        logger.error(traceback.format_exc())
        return HTTPException(
            status_code=500,
            detail="Erro interno do servidor. Verifique os logs para mais detalhes."
        )
    
    logger.info("API do chatbot inicializada com sucesso")
    return app 