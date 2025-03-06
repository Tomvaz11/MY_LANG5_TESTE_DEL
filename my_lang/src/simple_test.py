"""
Teste simplificado para a funcionalidade de perfis de usuário.
"""

from pydantic import BaseModel
from typing import List, Dict, Optional
import time


class UserProfile(BaseModel):
    """Modelo para o perfil do usuário."""
    name: Optional[str] = None
    preferred_name: Optional[str] = None
    language: Optional[str] = None
    interests: List[str] = []
    preferences: Dict[str, str] = {}
    expertise_level: Optional[str] = None


def test_simple_profile():
    """Teste básico de perfil de usuário sem dependências externas."""
    print("\n==================================================")
    print("Iniciando teste simplificado de perfil de usuário...")
    
    # Cria um perfil inicial
    print("\nCriando perfil inicial...")
    profile = UserProfile(
        name="Maria",
        preferred_name="Mari",
        language="Portuguese",
        interests=["música clássica", "jazz", "ficção científica"]
    )
    
    # Exibe o perfil inicial
    print("\nPerfil do usuário:")
    print(f"Nome: {profile.name}")
    print(f"Nome preferido: {profile.preferred_name}")
    print(f"Idioma: {profile.language}")
    print(f"Interesses: {', '.join(profile.interests)}")
    print(f"Preferências: {profile.preferences}")
    print(f"Expertise: {profile.expertise_level or 'Não especificado'}")
    
    # Atualiza o perfil
    print("\nAtualizando o perfil com novas informações...")
    
    # Atualiza o perfil com novas informações
    profile.name = "Mari"  # Usando nome preferido
    profile.interests = ["Desenvolvimento de aplicativos", "Inteligência Artificial", 
                        "Recomendação musical", "Python", "JavaScript"]
    profile.expertise_level = "Programadora"
    
    # Exibe o perfil atualizado
    print("\nPerfil atualizado do usuário:")
    print(f"Nome: {profile.name}")
    print(f"Nome preferido: {profile.preferred_name}")
    print(f"Idioma: {profile.language}")
    print(f"Interesses: {', '.join(profile.interests)}")
    print(f"Expertise: {profile.expertise_level}")
    
    # Verifica se o perfil foi atualizado corretamente
    assert profile.name == "Mari", "Nome não foi atualizado corretamente"
    assert profile.expertise_level == "Programadora", "Expertise não foi atualizada corretamente"
    assert "Inteligência Artificial" in profile.interests, "Interesses não foram atualizados corretamente"
    
    print("\nTeste simplificado concluído com sucesso!")


def simular_interacao_com_perfil():
    """
    Simula uma interação mais complexa com um perfil de usuário,
    demonstrando como seria usado em um chatbot real.
    """
    print("\n==================================================")
    print("Simulando interação de chatbot com perfil de usuário")
    
    # Cria um perfil inicial básico
    perfil = UserProfile(
        name="Usuário Anônimo",
        language="Português"
    )
    
    print("\nPerfil inicial (após primeiro contato):")
    print(f"Nome: {perfil.name}")
    print(f"Idioma: {perfil.language}")
    time.sleep(0.5)  # Pequena pausa para garantir que a saída seja exibida
    
    # Simula primeira interação onde o usuário se apresenta
    print("\nProcessando mensagem: 'Oi, meu nome é Carlos e gosto muito de tecnologia'")
    
    # Atualiza o perfil com base na mensagem
    perfil.name = "Carlos"
    perfil.interests.append("tecnologia")
    time.sleep(0.5)  # Pequena pausa
    
    print("\nPerfil atualizado:")
    print(f"Nome: {perfil.name}")
    print(f"Interesses: {', '.join(perfil.interests)}")
    time.sleep(0.5)  # Pequena pausa
    
    # Simula segunda interação com mais informações
    print("\nProcessando mensagem: 'Sou desenvolvedor Python e estou aprendendo IA'")
    
    # Atualiza o perfil novamente
    perfil.expertise_level = "Desenvolvedor"
    perfil.interests.extend(["Python", "Inteligência Artificial"])
    perfil.preferences["comunicação"] = "técnica"
    time.sleep(0.5)  # Pequena pausa
    
    print("\nPerfil final após todas as interações:")
    print(f"Nome: {perfil.name}")
    print(f"Expertise: {perfil.expertise_level}")
    print(f"Interesses: {', '.join(perfil.interests)}")
    print(f"Preferências: {perfil.preferences}")
    time.sleep(0.5)  # Pequena pausa
    
    # Simula como o chatbot usaria o perfil para personalizar respostas
    print("\nSimulando resposta personalizada do chatbot:")
    
    resposta = f"Olá {perfil.name}! Como um {perfil.expertise_level} interessado em "
    resposta += f"{', '.join(perfil.interests[:2])}, talvez você goste deste artigo sobre "
    resposta += "técnicas avançadas de processamento de linguagem natural usando Python."
    
    print(f"\nChatbot: {resposta}")
    print("\nSimulação concluída com sucesso!")


if __name__ == "__main__":
    # Executa o teste básico
    test_simple_profile()
    
    # Executa a simulação de interação
    simular_interacao_com_perfil() 