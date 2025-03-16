import pytest
from unittest.mock import MagicMock, patch
import time
from bot.eventos import (
    eventos_globais, evento_atual, evento_fim,
    iniciar_evento_aleatorio, verificar_fim_evento,
    obter_modificador_evento, esta_ativo_evento, obter_evento_atual
)
from bot.jogador import Jogador

class TestEventos:
    def test_iniciar_evento_aleatorio(self):
        """Testa a função iniciar_evento_aleatorio"""
        # Mocks
        bot_mock = MagicMock()
        jogadores_mock = {
            123: Jogador(user_id=123, username="jogador1"),
            456: Jogador(user_id=456, username="jogador2")
        }
        logger_mock = MagicMock()
        
        # Iniciar evento
        with patch('random.choice') as mock_choice:
            # Força a escolha do primeiro evento
            mock_choice.return_value = list(eventos_globais.items())[0]
            
            iniciar_evento_aleatorio(bot_mock, jogadores_mock, eventos_globais, logger_mock)
            
            # Verificações
            assert evento_atual is not None
            assert evento_fim > time.time()
            assert bot_mock.send_message.call_count == len(jogadores_mock)
            logger_mock.info.assert_called_once()
    
    def test_verificar_fim_evento(self):
        """Testa a função verificar_fim_evento"""
        # Mocks
        bot_mock = MagicMock()
        jogadores_mock = {
            123: Jogador(user_id=123, username="jogador1"),
            456: Jogador(user_id=456, username="jogador2")
        }
        logger_mock = MagicMock()
        
        # Configurar evento atual
        global evento_atual, evento_fim
        evento_atual = list(eventos_globais.keys())[0]
        evento_fim = time.time() - 10  # Evento já terminou
        
        # Verificar fim do evento
        verificar_fim_evento(bot_mock, jogadores_mock, logger_mock)
        
        # Verificações
        assert evento_atual is None
        assert bot_mock.send_message.call_count == len(jogadores_mock)
        logger_mock.info.assert_called_once()
    
    def test_obter_modificador_evento(self):
        """Testa a função obter_modificador_evento"""
        # Configurar jogador
        jogador = Jogador(user_id=123, username="jogador1")
        jogador.escolher_classe("Guerreiro")
        
        # Sem evento ativo
        global evento_atual, evento_fim
        evento_atual = None
        modificador = obter_modificador_evento(jogador, "ataque", 100)
        assert modificador == 100  # Sem modificação
        
        # Com evento ativo que afeta ataque
        evento_atual = "Chuva de Meteoros"  # Supondo que este evento afeta o ataque
        evento_fim = time.time() + 3600  # Evento ativo por mais 1 hora
        modificador = obter_modificador_evento(jogador, "ataque", 100)
        assert modificador != 100  # Com modificação
    
    def test_esta_ativo_evento(self):
        """Testa a função esta_ativo_evento"""
        # Sem evento ativo
        global evento_atual, evento_fim
        evento_atual = None
        assert not esta_ativo_evento()
        
        # Com evento ativo
        evento_atual = "Chuva de Meteoros"
        evento_fim = time.time() + 3600  # Evento ativo por mais 1 hora
        assert esta_ativo_evento()
        
        # Com evento expirado
        evento_fim = time.time() - 10  # Evento já terminou
        assert not esta_ativo_evento()
    
    def test_obter_evento_atual(self):
        """Testa a função obter_evento_atual"""
        # Sem evento ativo
        global evento_atual, evento_fim
        evento_atual = None
        info = obter_evento_atual()
        assert info["ativo"] is False
        
        # Com evento ativo
        evento_atual = "Chuva de Meteoros"
        evento_fim = time.time() + 3600  # Evento ativo por mais 1 hora
        info = obter_evento_atual()
        assert info["ativo"] is True
        assert info["nome"] == "Chuva de Meteoros"
        assert info["tempo_restante"] > 0
        assert "fim" in info 