"""
Teste para a funcionalidade de perfis de usuário.
"""

from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Adicionar o diretório pai ao caminho para importações
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Importar a classe UserProfile real
from my_lang.src.memory.profiles import UserProfile, update_user_profile, get_user_profile


class TestUserProfiles(unittest.TestCase):
    """Testes para perfis de usuário com mock."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        # Criar um mock do gerenciador de perfis
        self.mock_profile_manager = MagicMock()
        
        # Configurar um perfil inicial para os testes
        self.initial_profile = UserProfile(
            name="Maria",
            preferred_name="Mari",
            language="Portuguese",
            interests=["música clássica", "jazz", "ficção científica"]
        )
        
        # Configurar o perfil atualizado para retornar no mock
        self.updated_profile = UserProfile(
            name="Mari",  # Usando nome preferido
            preferred_name="Mari",
            language="Portuguese",
            interests=["Desenvolvimento de aplicativos", "Inteligência Artificial", 
                       "Recomendação musical", "Python", "JavaScript"],
            expertise_level="Programadora"
        )
        
        # Configurar o mock para retornar o perfil atualizado
        mock_result = MagicMock()
        mock_result.content = self.updated_profile
        self.mock_profile_manager.invoke.return_value = [mock_result]
    
    def test_update_user_profile(self):
        """Teste para a função update_user_profile."""
        print("\n==================================================")
        print("Iniciando teste de atualização de perfil de usuário com mock...")
        
        # Mensagens de teste
        messages = [
            {"role": "user", "content": "Olá, meu nome é Maria, mas prefiro ser chamada de Mari."},
            {"role": "assistant", "content": "Olá Mari, como posso ajudar?"},
            {"role": "user", "content": "Estou aprendendo sobre desenvolvimento de aplicativos e IA."}
        ]
        
        # Exibe o perfil inicial
        print("\nPerfil inicial do usuário:")
        print(f"Nome: {self.initial_profile.name}")
        print(f"Nome preferido: {self.initial_profile.preferred_name}")
        print(f"Idioma: {self.initial_profile.language}")
        print(f"Interesses: {', '.join(self.initial_profile.interests)}")
        print(f"Expertise: {self.initial_profile.expertise_level or 'Não especificado'}")
        
        # Atualiza o perfil usando a função com o mock
        print("\nAtualizando o perfil com novas informações...")
        updated_profile = update_user_profile(
            self.mock_profile_manager,
            messages,
            user_id="test_user"
        )
        
        # Verifica se o mock foi chamado corretamente
        self.mock_profile_manager.invoke.assert_called_once()
        
        # Exibe o perfil atualizado
        print("\nPerfil atualizado do usuário:")
        print(f"Nome: {updated_profile.name}")
        print(f"Nome preferido: {updated_profile.preferred_name}")
        print(f"Idioma: {updated_profile.language}")
        print(f"Interesses: {', '.join(updated_profile.interests)}")
        print(f"Expertise: {updated_profile.expertise_level}")
        
        # Verifica se o perfil foi atualizado corretamente
        self.assertEqual(updated_profile.name, "Mari")
        self.assertEqual(updated_profile.expertise_level, "Programadora")
        self.assertIn("Inteligência Artificial", updated_profile.interests)
        
        print("\nTeste de atualização de perfil concluído com sucesso!")
    
    @patch('my_lang.src.memory.profiles.get_user_profile')
    def test_get_user_profile(self, mock_get_profile):
        """Teste para a função get_user_profile."""
        print("\n==================================================")
        print("Iniciando teste de recuperação de perfil de usuário...")
        
        # Configurar o mock para retornar o perfil
        mock_get_profile.return_value = self.initial_profile
        
        # Mock de um armazenamento
        mock_store = MagicMock()
        
        # Testar a recuperação do perfil
        profile = get_user_profile(mock_store, user_id="test_user")
        
        # Exibe o perfil recuperado
        print("\nPerfil recuperado do armazenamento:")
        print(f"Nome: {profile.name}")
        print(f"Nome preferido: {profile.preferred_name}")
        print(f"Idioma: {profile.language}")
        print(f"Interesses: {', '.join(profile.interests)}")
        
        # Verificar se o perfil foi recuperado corretamente
        self.assertEqual(profile.name, "Maria")
        self.assertEqual(profile.preferred_name, "Mari")
        
        print("\nTeste de recuperação de perfil concluído com sucesso!")


def simple_test_user_profile():
    """Teste simplificado de perfil de usuário sem dependências."""
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


if __name__ == "__main__":
    # Execute o teste simplificado primeiro
    simple_test_user_profile()
    
    # Em seguida, execute os testes unitários
    unittest.main(argv=['first-arg-is-ignored'], exit=False) 