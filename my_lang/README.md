# Chatbot com Memória LangMem

Um chatbot inteligente que utiliza a tecnologia LangMem para gerenciar memória de longo prazo, permitindo conversas contextuais e personalizadas ao longo do tempo.

## Recursos

- ✅ Memória semântica usando LangMem
- ✅ Ferramentas para gerenciar e buscar memórias
- ✅ Recuperação de memórias relevantes durante a conversa
- ✅ Processamento de memória em segundo plano
- ✅ Perfis de usuário para personalização
- ✅ Interface web simples com FastAPI
- ✅ Suporte a armazenamento persistente com PostgreSQL

## Instalação

1. Clone este repositório:
```bash
git clone <repo-url>
cd my_lang
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
```bash
cp .env.example .env
```
Edite o arquivo `.env` e adicione sua chave API da OpenAI.

## Executando o Chatbot

```bash
python -m src.app
```

Acesse a interface web em http://localhost:8000

## Armazenamento Persistente com PostgreSQL

Por padrão, o chatbot utiliza um armazenamento em memória (`InMemoryStore`) que é volátil e se perde quando a aplicação é reiniciada. Para habilitar a persistência dos dados de memória, você pode configurar o PostgreSQL.

### Configuração do PostgreSQL

1. Instale o PostgreSQL e a extensão pgvector:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo apt install postgresql-server-dev-15 # ou sua versão do PostgreSQL

# Instale a extensão pgvector
git clone https://github.com/pgvector/pgvector.git
cd pgvector
make
sudo make install
```

2. Crie um banco de dados:
```bash
sudo -u postgres psql
CREATE DATABASE chatbot_db;
CREATE USER chatbot_user WITH PASSWORD 'sua_senha';
GRANT ALL PRIVILEGES ON DATABASE chatbot_db TO chatbot_user;
\c chatbot_db
CREATE EXTENSION IF NOT EXISTS vector;
\q
```

3. Configure as variáveis de ambiente no arquivo `.env`:
```
USE_POSTGRES=true
POSTGRES_CONNECTION_STRING=postgresql://chatbot_user:sua_senha@localhost:5432/chatbot_db
POSTGRES_POOL_MIN_SIZE=2
POSTGRES_POOL_MAX_SIZE=10
```

### Verificação da Instalação

Para verificar se o PostgreSQL está sendo utilizado corretamente, você pode observar os logs da aplicação na inicialização. A primeira vez que o chatbot for iniciado com o PostgreSQL configurado, ele executará as migrações necessárias e criará as tabelas automaticamente.

## Estrutura do Projeto

- `src/`: Código fonte do chatbot
  - `memory/`: Implementação da memória usando LangMem
    - `background.py`: Processamento de memória em segundo plano
    - `manager.py`: Gerenciamento de memórias
    - `optimizer.py`: Otimização de prompts do sistema
    - `profiles.py`: Gerenciamento de perfis de usuário
  - `agent/`: Implementação do agente conversacional
    - `chat_agent.py`: Agente de chat com suporte a memória
  - `api/`: API e interfaces para interagir com o chatbot
    - `routes.py`: Rotas da API
    - `static/`: Arquivos estáticos da interface web
  - `app.py`: Aplicação principal 
  - `config.py`: Configurações do chatbot
- `tests/`: Testes unitários e de integração

## Variáveis de Ambiente

O chatbot pode ser configurado através das seguintes variáveis de ambiente:

- `OPENAI_API_KEY`: Chave de API da OpenAI (obrigatória)
- `MODEL_NAME`: Modelo de linguagem a ser usado (padrão: "gpt-4o-mini")
- `EMBEDDING_MODEL`: Modelo para embeddings (padrão: "openai:text-embedding-3-small")
- `BACKGROUND_MEMORY_DELAY`: Atraso para processamento de memória em segundo plano (padrão: 60.0 segundos)
- `API_HOST`: Host para a API (padrão: "0.0.0.0")
- `API_PORT`: Porta para a API (padrão: 8000)
- `USE_POSTGRES`: Habilita o armazenamento persistente com PostgreSQL (padrão: "false")
- `POSTGRES_CONNECTION_STRING`: String de conexão para o PostgreSQL
- `POSTGRES_POOL_MIN_SIZE`: Tamanho mínimo do pool de conexões (padrão: 2)
- `POSTGRES_POOL_MAX_SIZE`: Tamanho máximo do pool de conexões (padrão: 10)

## Tecnologias Utilizadas

- [LangMem](https://github.com/langchain-ai/langmem): Gerenciamento de memória para agentes de IA
- [LangGraph](https://github.com/langchain-ai/langgraph): Estruturação de fluxos de conversa
- [LangChain](https://github.com/langchain-ai/langchain): Framework para aplicações com LLMs
- [OpenAI](https://openai.com/): Modelos de linguagem
- [FastAPI](https://fastapi.tiangolo.com/): Framework web para a API
- [PostgreSQL](https://www.postgresql.org/): Banco de dados relacional para armazenamento persistente
- [pgvector](https://github.com/pgvector/pgvector): Extensão PostgreSQL para suporte a vetores

## Funcionalidades

- **Memória Semântica**: Armazena e recupera informações importantes das conversas.
- **Memória em Segundo Plano**: Processa informações importantes das conversas para uso futuro.
- **Otimização de Prompts**: Melhora automaticamente os prompts do sistema com base nas interações.
- **Perfis de Usuário**: Armazena e gerencia informações sobre os usuários para personalizar as respostas.
- **Armazenamento Persistente**: Suporte opcional para armazenar memórias e perfis em um banco de dados PostgreSQL.

## Uso Programático

### Criação do Agente

```python
from src.agent import create_chat_agent

# Cria o agente com suporte a memória em segundo plano e perfis de usuário
agent_components = create_chat_agent(
    enable_background_memory=True,
    enable_user_profiles=True,
)

agent = agent_components["agent"]
background_memory_manager = agent_components["background_memory_manager"]
profile_manager = agent_components["profile_manager"]
```

### Envio de Mensagens

```python
from src.agent import chat

resposta = chat(
    agent=agent,
    message="Olá, meu nome é João!",
    user_id="user_123",
    background_memory_manager=background_memory_manager,
    profile_manager=profile_manager,
)

print(resposta)
```

## Licença

Este projeto é distribuído sob a licença MIT. 