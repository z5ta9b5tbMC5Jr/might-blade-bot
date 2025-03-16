import pytest
from bot.jogador import Jogador

class TestJogador:
    def test_criar_jogador(self):
        """Testa a criação de um jogador"""
        jogador = Jogador(user_id=123456789, username="testuser")
        assert jogador.user_id == 123456789
        assert jogador.username == "testuser"
        assert jogador.classe is None
        assert jogador.nivel == 1
        assert jogador.experiencia == 0
        assert jogador.moedas == 100
        assert jogador.vida == 100
        assert jogador.vida_maxima == 100
        
    def test_escolher_classe(self):
        """Testa a escolha de classe do jogador"""
        jogador = Jogador(user_id=123456789, username="testuser")
        
        # Teste para classe Guerreiro
        jogador.escolher_classe("Guerreiro")
        assert jogador.classe == "Guerreiro"
        assert jogador.ataque > 0
        assert jogador.defesa > 0
        
        # Teste para classe Mago
        jogador = Jogador(user_id=123456789, username="testuser")
        jogador.escolher_classe("Mago")
        assert jogador.classe == "Mago"
        assert jogador.ataque > 0
        assert jogador.defesa > 0
        
        # Teste para classe Arqueiro
        jogador = Jogador(user_id=123456789, username="testuser")
        jogador.escolher_classe("Arqueiro")
        assert jogador.classe == "Arqueiro"
        assert jogador.ataque > 0
        assert jogador.defesa > 0
        
    def test_ganhar_experiencia(self):
        """Testa o ganho de experiência e subida de nível"""
        jogador = Jogador(user_id=123456789, username="testuser")
        jogador.escolher_classe("Guerreiro")
        
        # Nível inicial
        assert jogador.nivel == 1
        assert jogador.experiencia == 0
        
        # Ganhar experiência insuficiente para subir de nível
        subiu, _ = jogador.ganhar_experiencia(50)
        assert not subiu
        assert jogador.nivel == 1
        assert jogador.experiencia == 50
        
        # Ganhar experiência suficiente para subir de nível
        subiu, _ = jogador.ganhar_experiencia(100)
        assert subiu
        assert jogador.nivel == 2
        assert jogador.experiencia == 50  # 150 - 100 (exp para nível 2)
        
    def test_receber_dano(self):
        """Testa o recebimento de dano"""
        jogador = Jogador(user_id=123456789, username="testuser")
        jogador.escolher_classe("Guerreiro")
        jogador.vida = 100
        
        # Receber dano
        jogador.receber_dano(30)
        assert jogador.vida == 70
        
        # Receber dano fatal
        jogador.receber_dano(100)
        assert jogador.vida == 0
        
    def test_curar(self):
        """Testa a cura do jogador"""
        jogador = Jogador(user_id=123456789, username="testuser")
        jogador.escolher_classe("Guerreiro")
        jogador.vida = 50
        
        # Cura parcial
        jogador.curar(20)
        assert jogador.vida == 70
        
        # Cura além do máximo
        jogador.curar(50)
        assert jogador.vida == jogador.vida_maxima 