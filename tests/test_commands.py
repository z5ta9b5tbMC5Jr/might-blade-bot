import pytest
from unittest.mock import Mock
import sys
import os

# Ajuste para importações absolutas
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bot.bot import Database, Jogador
from bot.errors import CustomError
from bot.utils import rate_limit

@pytest.fixture
def mock_db():
    db = Database(":memory:")
    db.create_tables()
    return db

def test_save_player(mock_db):
    player = Jogador(1, "Teste", "Guerreiro")
    assert mock_db.salvar_jogador(player) is True

def test_rate_limit_exceeded():
    mock_message = Mock()
    mock_message.from_user.id = 123
    
    # Testar exceder o rate limit
    with pytest.raises(CustomError):
        for _ in range(6):
            rate_limit(lambda x: x)(mock_message) 