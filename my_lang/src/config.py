"""
Configurações para o chatbot com LangMem.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
dotenv_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=dotenv_path)

# Configurações do modelo
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")  # Modelo principal
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "openai:text-embedding-3-small")  # Modelo para embeddings

# Configurações de memória
MEMORY_NAMESPACE = ("chatbot_memories", "{user_id}")
DEFAULT_USER_ID = "default_user"

# Configurações para o PostgreSQL
USE_POSTGRES = os.getenv("USE_POSTGRES", "false").lower() == "true"
POSTGRES_CONNECTION_STRING = os.getenv("POSTGRES_CONNECTION_STRING", "postgresql://postgres:postgres@localhost:5432/postgres")
POSTGRES_POOL_MIN_SIZE = int(os.getenv("POSTGRES_POOL_MIN_SIZE", "2"))
POSTGRES_POOL_MAX_SIZE = int(os.getenv("POSTGRES_POOL_MAX_SIZE", "10"))

# Configurações para processamento de memória em segundo plano
BACKGROUND_MEMORY_DELAY = float(os.getenv("BACKGROUND_MEMORY_DELAY", "60.0"))  # Tempo de atraso em segundos
MEMORY_QUERY_LIMIT = int(os.getenv("MEMORY_QUERY_LIMIT", "5"))  # Número máximo de memórias a recuperar

# Instruções para as ferramentas de memória
MEMORY_INSTRUCTIONS = """
Proativamente chame esta ferramenta quando você:

1. Identificar uma nova preferência do USUÁRIO.
2. Receber um pedido explícito do USUÁRIO para se lembrar de algo ou alterar seu comportamento.
3. Estiver trabalhando e quiser registrar um contexto importante.
4. Identificar que uma MEMÓRIA existente está incorreta ou desatualizada.
"""

SEARCH_INSTRUCTIONS = """
Use esta ferramenta para buscar informações relevantes em suas memórias existentes quando:

1. O usuário faz uma pergunta que pode estar relacionada com informações previamente compartilhadas
2. Você precisa verificar preferências ou informações pessoais do usuário que podem ter sido mencionadas anteriormente
3. Você precisa manter consistência com informações fornecidas em conversas anteriores
"""

# Instruções do sistema para o chatbot
SYSTEM_INSTRUCTIONS = """
Você é um assistente útil e gentil que se lembra das conversas anteriores com os usuários.
Use suas ferramentas de memória para armazenar informações importantes e recuperá-las quando necessário.
Seja natural e conversacional, evitando mencionar explicitamente suas "memórias" ou "ferramentas" para o usuário.
Mantenha consistência com o que o usuário compartilhou anteriormente e seja atencioso com suas preferências.
"""

# Configurações da API
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# Chaves de API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") 