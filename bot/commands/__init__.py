from .hello import setup as setup_hello
from .music import setup as setup_music
from .ping import setup as setup_ping

# Lista de todas as funções setup dos comandos disponíveis
__all__ = ["setup_hello", "setup_music", "setup_ping"]
