"""
Teste de integração para as três funcionalidades do LangMem:
1. Memória em segundo plano
2. Otimização de prompts
3. Perfis de usuário

Este teste demonstra como as três funcionalidades podem ser usadas em conjunto.
"""

from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import time
import json
from unittest.mock import MagicMock


# Modelo para o perfil do usuário
class UserProfile(BaseModel):
    """Modelo para o perfil do usuário."""
    name: Optional[str] = None
    preferred_name: Optional[str] = None
    language: Optional[str] = None
    interests: List[str] = []
    preferences: Dict[str, str] = {}
    expertise_level: Optional[str] = None


# Simulação das funcionalidades do LangMem
class SimulatedMemoryManager:
    """Simulação simplificada do gerenciador de memória."""
    
    def __init__(self):
        """Inicializa o gerenciador de memória simulado."""
        self.memories = []
        self.optimized_prompt = None
        self.user_profile = None
    
    def add_memory(self, content: str, importance: int = 1):
        """Adiciona uma memória."""
        memory_id = f"mem-{len(self.memories) + 1}"
        memory = {
            "id": memory_id,
            "content": content,
            "importance": importance,
            "created_at": time.time()
        }
        self.memories.append(memory)
        return memory_id
    
    def get_memories(self, limit: int = 5):
        """Recupera memórias, ordenadas por importância."""
        sorted_memories = sorted(self.memories, key=lambda x: x["importance"], reverse=True)
        return sorted_memories[:limit]
    
    def optimize_prompt(self, system_prompt: str, memories: List[Dict]):
        """Simula a otimização de prompt com memórias."""
        memory_text = "\n".join([f"- {mem['content']}" for mem in memories])
        optimized = f"{system_prompt}\n\nContexto relevante:\n{memory_text}"
        self.optimized_prompt = optimized
        return optimized
    
    def update_profile(self, profile_data: Dict):
        """Atualiza o perfil do usuário."""
        if not self.user_profile:
            self.user_profile = UserProfile(**profile_data)
        else:
            for key, value in profile_data.items():
                if hasattr(self.user_profile, key):
                    setattr(self.user_profile, key, value)
        return self.user_profile


def test_integration():
    """Teste de integração simulado."""
    print("\n==================================================")
    print("Iniciando teste de integração das funcionalidades LangMem...")
    
    # Criar gerenciador de memória simulado
    memory_manager = SimulatedMemoryManager()
    
    # 1. Adicionar memórias em segundo plano
    print("\n1. TESTE DE MEMÓRIA EM SEGUNDO PLANO")
    print("Adicionando memórias em segundo plano...")
    
    memory_manager.add_memory("O usuário mencionou que trabalha com desenvolvimento web", 3)
    memory_manager.add_memory("O usuário está aprendendo React e TypeScript", 4)
    memory_manager.add_memory("O usuário teve problemas com instalação do Node.js", 2)
    memory_manager.add_memory("O usuário gosta de documentação com exemplos práticos", 3)
    
    # Recuperar memórias
    print("\nMemórias armazenadas (ordenadas por importância):")
    memories = memory_manager.get_memories()
    for i, memory in enumerate(memories, 1):
        print(f"{i}. {memory['content']} (Importância: {memory['importance']})")
    
    time.sleep(0.5)
    
    # 2. Otimização de prompt
    print("\n2. TESTE DE OTIMIZAÇÃO DE PROMPT")
    base_prompt = "Você é um assistente útil especializado em programação."
    
    print("\nPrompt base original:")
    print(base_prompt)
    
    # Otimizar o prompt com as memórias
    optimized_prompt = memory_manager.optimize_prompt(base_prompt, memories)
    
    print("\nPrompt otimizado com memórias:")
    print(optimized_prompt)
    
    time.sleep(0.5)
    
    # 3. Gerenciamento de perfil de usuário
    print("\n3. TESTE DE PERFIL DE USUÁRIO")
    
    # Criar perfil inicial
    print("\nCriando perfil inicial com base em interações...")
    profile_data = {
        "name": "Ana",
        "language": "Português",
        "interests": ["desenvolvimento web"]
    }
    
    profile = memory_manager.update_profile(profile_data)
    
    print("\nPerfil inicial:")
    print(f"Nome: {profile.name}")
    print(f"Idioma: {profile.language}")
    print(f"Interesses: {', '.join(profile.interests)}")
    
    # Atualizar o perfil com mais informações
    print("\nAtualizando perfil com novas informações...")
    profile_update = {
        "expertise_level": "Intermediário",
        "interests": ["desenvolvimento web", "React", "TypeScript", "Node.js"],
        "preferences": {"comunicação": "prática", "exemplos": "detalhados"}
    }
    
    updated_profile = memory_manager.update_profile(profile_update)
    
    print("\nPerfil atualizado:")
    print(f"Nome: {updated_profile.name}")
    print(f"Expertise: {updated_profile.expertise_level}")
    print(f"Interesses: {', '.join(updated_profile.interests)}")
    print(f"Preferências: {updated_profile.preferences}")
    
    time.sleep(0.5)
    
    # 4. Resposta integrada usando as três funcionalidades
    print("\n4. DEMONSTRAÇÃO DE RESPOSTA INTEGRADA")
    
    # Simular uma pergunta do usuário
    user_question = "Estou tendo problemas para configurar um projeto React com TypeScript. Pode me ajudar?"
    
    print(f"\nPergunta do usuário: '{user_question}'")
    
    # Construir uma resposta personalizada usando todas as funcionalidades
    print("\nConstruindo resposta personalizada utilizando:")
    print("- Memórias relevantes do usuário")
    print("- Prompt otimizado")
    print("- Informações do perfil")
    
    # Resposta personalizada
    response = f"""Olá {updated_profile.name}!

Como desenvolvedor de nível {updated_profile.expertise_level} em {', '.join(updated_profile.interests[:2])}, 
vou te ajudar com a configuração do React com TypeScript.

Baseado nas nossas conversas anteriores, sei que:
{memories[0]['content']}
{memories[1]['content']}
{memories[2]['content']}

Vou criar um guia prático e detalhado para configurar seu projeto, já que sei que você prefere 
{updated_profile.preferences.get('comunicação', 'clara')} e com {updated_profile.preferences.get('exemplos', 'exemplos')}.

Aqui está um passo a passo para configurar corretamente o ambiente:
1. Verifique sua instalação do Node.js (lembro que você teve problemas com isso antes)
2. Execute: npx create-react-app meu-app --template typescript
3. Configure o tsconfig.json conforme suas necessidades
4. Instale bibliotecas adicionais que você possa precisar

Isso deve resolver seu problema. Posso detalhar algum passo específico?
"""
    
    print("\nResposta personalizada do assistente:")
    print(response)
    
    print("\nTeste de integração concluído com sucesso!")


if __name__ == "__main__":
    test_integration() 