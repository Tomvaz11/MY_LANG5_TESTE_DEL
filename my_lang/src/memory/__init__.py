"""
Módulo para gerenciamento de memória usando LangMem.
"""

from src.memory.manager import (
    create_memory_store,
    create_memory_prompt_function,
)

from src.memory.background import (
    create_background_memory_manager,
    schedule_memory_processing,
)

from src.memory.optimizer import (
    create_system_prompt_optimizer,
    optimize_system_prompt,
    create_multi_system_prompt_optimizer,
    optimize_multiple_prompts,
)

from src.memory.profiles import (
    UserProfile,
    create_profile_manager,
    create_profile_store_manager,
    get_user_profile,
    update_user_profile,
)

__all__ = [
    "create_memory_store",
    "create_memory_prompt_function",
    "create_background_memory_manager",
    "schedule_memory_processing",
    "create_system_prompt_optimizer",
    "optimize_system_prompt",
    "create_multi_system_prompt_optimizer",
    "optimize_multiple_prompts",
    "UserProfile",
    "create_profile_manager",
    "create_profile_store_manager",
    "get_user_profile",
    "update_user_profile",
] 