"""
Script de instalação para o chatbot com LangMem.
"""

from setuptools import setup, find_packages

setup(
    name="my_lang",
    version="1.0.0",
    description="Um chatbot com memória de longo prazo usando LangMem",
    author="Seu Nome",
    author_email="seu.email@exemplo.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "langchain>=0.3.15",
        "langchain-openai>=0.3.1",
        "openai>=1.20.0",
        "langmem>=0.0.13",
        "langgraph>=0.2.66",
        "langgraph-checkpoint>=2.0.12",
        "python-dotenv>=1.0.0",
        "fastapi>=0.109.2",
        "uvicorn>=0.27.1",
    ],
    entry_points={
        "console_scripts": [
            "my_lang=my_lang.src.app:main",
        ],
    },
    python_requires=">=3.10",
) 