import pytest
import sys
import os
from unittest.mock import MagicMock

# Adiciona o diretório raiz ao path para importar os módulos do bot
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def mock_bot():
    """Fixture que retorna um mock do objeto bot"""
    mock = MagicMock()
    return mock

@pytest.fixture
def mock_update():
    """Fixture que retorna um mock do objeto Update"""
    mock = MagicMock()
    mock.effective_user.id = 123456789
    mock.effective_user.username = "testuser"
    mock.effective_chat.id = 123456789
    mock.message.text = "/comando"
    return mock

@pytest.fixture
def mock_context():
    """Fixture que retorna um mock do objeto Context"""
    mock = MagicMock()
    return mock

@pytest.fixture
def mock_db():
    """Fixture que retorna um mock do objeto Database"""
    mock = MagicMock()
    return mock

@pytest.fixture
def mock_jogadores():
    """Fixture que retorna um mock do dicionário de jogadores"""
    return {} 