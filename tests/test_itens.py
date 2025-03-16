import pytest
from bot.itens import (
    armas, armaduras, amuletos, consumiveis,
    obter_item_por_nome, itens_por_classe, aplicar_efeito_item
)
from bot.jogador import Jogador

class TestItens:
    def test_obter_item_por_nome(self):
        """Testa a função obter_item_por_nome"""
        # Teste para arma
        espada = obter_item_por_nome("Espada Longa")
        assert espada is not None
        assert espada["tipo"] == "arma"
        assert espada["dano"] > 0
        
        # Teste para armadura
        armadura = obter_item_por_nome("Armadura de Couro")
        assert armadura is not None
        assert armadura["tipo"] == "armadura"
        assert armadura["defesa"] > 0
        
        # Teste para amuleto
        amuleto = obter_item_por_nome("Amuleto de Força")
        assert amuleto is not None
        assert amuleto["tipo"] == "amuleto"
        
        # Teste para consumível
        pocao = obter_item_por_nome("Poção de Vida")
        assert pocao is not None
        assert pocao["tipo"] == "consumivel"
        
        # Teste para item inexistente
        item_inexistente = obter_item_por_nome("Item Inexistente")
        assert item_inexistente is None
    
    def test_itens_por_classe(self):
        """Testa a função itens_por_classe"""
        # Teste para Guerreiro
        itens_guerreiro = itens_por_classe("Guerreiro")
        assert len(itens_guerreiro["armas"]) > 0
        assert len(itens_guerreiro["armaduras"]) > 0
        assert len(itens_guerreiro["amuletos"]) > 0
        
        # Teste para Mago
        itens_mago = itens_por_classe("Mago")
        assert len(itens_mago["armas"]) > 0
        assert len(itens_mago["armaduras"]) > 0
        assert len(itens_mago["amuletos"]) > 0
        
        # Teste para Arqueiro
        itens_arqueiro = itens_por_classe("Arqueiro")
        assert len(itens_arqueiro["armas"]) > 0
        assert len(itens_arqueiro["armaduras"]) > 0
        assert len(itens_arqueiro["amuletos"]) > 0
        
        # Teste para classe inexistente
        itens_invalidos = itens_por_classe("Classe Inexistente")
        assert itens_invalidos["armas"] == []
        assert itens_invalidos["armaduras"] == []
        assert itens_invalidos["amuletos"] == []
    
    def test_aplicar_efeito_item(self):
        """Testa a função aplicar_efeito_item"""
        jogador = Jogador(user_id=123456789, username="testuser")
        jogador.escolher_classe("Guerreiro")
        jogador.vida = 50
        
        # Teste para poção de vida
        pocao_vida = obter_item_por_nome("Poção de Vida")
        resultado = aplicar_efeito_item(jogador, pocao_vida)
        assert resultado["sucesso"]
        assert jogador.vida > 50
        
        # Teste para poção de força
        ataque_inicial = jogador.ataque
        pocao_forca = obter_item_por_nome("Poção de Força")
        resultado = aplicar_efeito_item(jogador, pocao_forca)
        assert resultado["sucesso"]
        assert jogador.ataque > ataque_inicial
        
        # Teste para item não consumível
        espada = obter_item_por_nome("Espada Longa")
        resultado = aplicar_efeito_item(jogador, espada)
        assert not resultado["sucesso"]
        assert "não é um item consumível" in resultado["mensagem"] 