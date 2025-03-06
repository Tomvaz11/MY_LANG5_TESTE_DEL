"""
Otimização de prompts usando LangMem.

Este módulo implementa funcionalidades para otimizar os prompts do sistema com base em
feedback do usuário e análise de interações.
"""

from typing import Dict, List, Any, Optional

from langmem import create_prompt_optimizer, create_multi_prompt_optimizer
from langgraph.store.memory import InMemoryStore

from src.config import MODEL_NAME


def create_system_prompt_optimizer(
    model_name: str = MODEL_NAME,
    max_reflection_steps: int = 3,
):
    """
    Cria um otimizador de prompts do sistema.
    
    O otimizador analisa interações passadas e feedback para melhorar os prompts
    do sistema, tornando o agente mais eficaz ao longo do tempo.
    
    Args:
        model_name (str): Nome do modelo de linguagem
        max_reflection_steps (int): Número máximo de etapas de reflexão
        
    Returns:
        callable: Função para otimizar prompts do sistema
    """
    optimizer = create_prompt_optimizer(
        model_name,
        kind="metaprompt",
        config={"max_reflection_steps": max_reflection_steps}
    )
    
    return optimizer


def optimize_system_prompt(
    optimizer,
    current_prompt: str,
    trajectories: List[Dict[str, Any]],
    feedback: Dict[str, Any],
) -> str:
    """
    Otimiza um prompt do sistema com base em interações e feedback.
    
    Args:
        optimizer: Otimizador de prompts
        current_prompt (str): Prompt atual do sistema
        trajectories (List[Dict[str, Any]]): Histórico de interações
        feedback (Dict[str, Any]): Feedback do usuário ou sistema
        
    Returns:
        str: Prompt otimizado
    """
    # Formata as trajetórias com feedback
    formatted_trajectories = [(trajectory, feedback) for trajectory in trajectories]
    
    # Invoca o otimizador
    optimized_prompt = optimizer.invoke({
        "prompt": current_prompt,
        "trajectories": formatted_trajectories
    })
    
    return optimized_prompt


def create_multi_system_prompt_optimizer(
    model_name: str = MODEL_NAME,
    max_reflection_steps: int = 3,
):
    """
    Cria um otimizador para múltiplos prompts do sistema.
    
    Útil quando há diferentes componentes do sistema com diferentes instruções
    que precisam ser otimizadas de forma coerente.
    
    Args:
        model_name (str): Nome do modelo de linguagem
        max_reflection_steps (int): Número máximo de etapas de reflexão
        
    Returns:
        callable: Função para otimizar múltiplos prompts do sistema
    """
    multi_optimizer = create_multi_prompt_optimizer(
        model_name,
        kind="metaprompt",
        config={"max_reflection_steps": max_reflection_steps}
    )
    
    return multi_optimizer


def optimize_multiple_prompts(
    multi_optimizer,
    prompts: Dict[str, str],
    trajectories: List[Dict[str, Any]],
    feedback: Dict[str, Any],
) -> Dict[str, str]:
    """
    Otimiza múltiplos prompts do sistema com base em interações e feedback.
    
    Args:
        multi_optimizer: Otimizador de múltiplos prompts
        prompts (Dict[str, str]): Dicionário de prompts atuais
        trajectories (List[Dict[str, Any]]): Histórico de interações
        feedback (Dict[str, Any]): Feedback do usuário ou sistema
        
    Returns:
        Dict[str, str]: Dicionário de prompts otimizados
    """
    # Formata as trajetórias com feedback
    formatted_trajectories = [(trajectory, feedback) for trajectory in trajectories]
    
    # Invoca o otimizador de múltiplos prompts
    optimized_prompts = multi_optimizer.invoke({
        "prompts": prompts,
        "trajectories": formatted_trajectories
    })
    
    return optimized_prompts 