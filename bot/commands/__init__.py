# bot/commands/__init__.py

from .hello import setup as setup_hello
from .music import setup as setup_music

# Lista de todas as funções setup dos comandos disponíveis
__all__ = ["setup_hello", "setup_play"]
