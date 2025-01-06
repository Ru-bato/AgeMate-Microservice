# config/__init__.py
from .settings import Settings
from .logging import setup_logging

settings = Settings()
setup_logging(settings)