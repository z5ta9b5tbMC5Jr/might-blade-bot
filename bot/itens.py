# Definições de itens para o jogo
# Cada dicionário contém informações sobre um tipo específico de item

# Armas disponíveis no jogo
armas = {
    # Armas para Guerreiro
    "Espada Básica": {"dano": 5, "preco": 50, "classe": "Guerreiro", "descricao": "Uma espada simples mas eficiente."},
    "Espada Longa": {"dano": 8, "preco": 100, "classe": "Guerreiro", "descricao": "Uma espada de alcance maior e mais poder."},
    "Machado de Batalha": {"dano": 10, "preco": 150, "classe": "Guerreiro", "descricao": "Um machado pesado que causa dano devastador."},
    "Martelo de Guerra": {"dano": 12, "preco": 200, "classe": "Guerreiro", "descricao": "Um martelo poderoso que pode esmagar armaduras."},
    "Espada Flamejante": {"dano": 15, "preco": 300, "classe": "Guerreiro", "descricao": "Uma espada encantada com o poder do fogo."},
    
    # Armas para Arqueiro
    "Adaga Afiada": {"dano": 3, "preco": 30, "classe": "Arqueiro", "descricao": "Uma adaga leve e precisa."},
    "Arco Curto": {"dano": 5, "preco": 60, "classe": "Arqueiro", "descricao": "Um arco simples mas eficaz para iniciantes."},
    "Arco Élfico": {"dano": 7, "preco": 120, "classe": "Arqueiro", "descricao": "Um arco élfico refinado e preciso."},
    "Besta de Repetição": {"dano": 9, "preco": 180, "classe": "Arqueiro", "descricao": "Uma besta que permite disparos rápidos e precisos."},
    "Arco Longo de Precisão": {"dano": 12, "preco": 250, "classe": "Arqueiro", "descricao": "Um arco longo que permite atingir alvos distantes com precisão mortal."},
    
    # Armas para Mago
    "Cajado Iniciante": {"dano": 4, "preco": 40, "classe": "Mago", "descricao": "Um cajado para canalizar magia básica."},
    "Varinha Arcana": {"dano": 6, "preco": 80, "classe": "Mago", "descricao": "Uma varinha que amplifica feitiços básicos."},
    "Cajado Elemental": {"dano": 9, "preco": 130, "classe": "Mago", "descricao": "Um cajado que potencializa magias elementais."},
    "Orbe Místico": {"dano": 11, "preco": 200, "classe": "Mago", "descricao": "Um orbe que concentra energia mágica para feitiços poderosos."},
    "Cajado do Arquimago": {"dano": 14, "preco": 280, "classe": "Mago", "descricao": "Um cajado lendário que amplifica drasticamente o poder mágico."}
}

# Armaduras disponíveis no jogo
armaduras = {
    # Armaduras para Arqueiro
    "Armadura de Couro": {"defesa": 3, "preco": 40, "classe": "Arqueiro", "descricao": "Armadura leve feita de couro resistente."},
    "Capa do Caçador": {"defesa": 4, "preco": 70, "classe": "Arqueiro", "descricao": "Uma capa que oferece camuflagem e proteção leve."},
    "Armadura de Escamas": {"defesa": 6, "preco": 120, "classe": "Arqueiro", "descricao": "Armadura feita de escamas leves mas resistentes."},
    "Traje Élfico": {"defesa": 8, "preco": 180, "classe": "Arqueiro", "descricao": "Um traje élfico que combina leveza e proteção superior."},
    
    # Armaduras para Guerreiro
    "Armadura de Ferro": {"defesa": 5, "preco": 80, "classe": "Guerreiro", "descricao": "Armadura robusta que oferece boa proteção."},
    "Armadura de Placas": {"defesa": 8, "preco": 150, "classe": "Guerreiro", "descricao": "Armadura pesada que oferece excelente proteção."},
    "Armadura de Cavaleiro": {"defesa": 10, "preco": 220, "classe": "Guerreiro", "descricao": "Armadura completa digna de um cavaleiro real."},
    "Armadura Encantada": {"defesa": 12, "preco": 300, "classe": "Guerreiro", "descricao": "Armadura reforçada com encantamentos de proteção."},
    
    # Armaduras para Mago
    "Vestes Arcanas": {"defesa": 2, "mana": 10, "preco": 60, "classe": "Mago", "descricao": "Vestes que aumentam seu poder mágico."},
    "Manto do Sábio": {"defesa": 3, "mana": 15, "preco": 100, "classe": "Mago", "descricao": "Um manto que amplifica a regeneração de mana."},
    "Vestes Elementais": {"defesa": 4, "mana": 20, "preco": 160, "classe": "Mago", "descricao": "Vestes imbuídas com poder elemental que aumentam a potência de magias."},
    "Manto do Arquimago": {"defesa": 5, "mana": 30, "preco": 250, "classe": "Mago", "descricao": "Um manto lendário que oferece grande proteção mágica e reserva de mana."}
}

# Amuletos disponíveis no jogo
amuletos = {
    # Amuletos para todas as classes
    "Amuleto de Proteção": {"efeito": "defesa", "valor": 2, "preco": 50, "classe": "Qualquer", "descricao": "Um amuleto que oferece proteção adicional contra ataques."},
    "Amuleto da Sorte": {"efeito": "sorte", "valor": 5, "preco": 75, "classe": "Qualquer", "descricao": "Aumenta suas chances de encontrar itens raros."},
    "Amuleto de Vitalidade": {"efeito": "vida", "valor": 15, "preco": 90, "classe": "Qualquer", "descricao": "Aumenta a vida máxima do personagem."},
    
    # Amuletos para Guerreiro
    "Amuleto do Guerreiro": {"efeito": "forca", "valor": 3, "preco": 100, "classe": "Guerreiro", "descricao": "Aumenta a força do guerreiro em combate."},
    "Amuleto do Berserker": {"efeito": "furia", "valor": 5, "preco": 150, "classe": "Guerreiro", "descricao": "Aumenta o dano causado quando a vida está baixa."},
    "Amuleto do Campeão": {"efeito": "resistencia", "valor": 4, "preco": 200, "classe": "Guerreiro", "descricao": "Reduz o dano recebido em combate."},
    
    # Amuletos para Mago
    "Amuleto Arcano": {"efeito": "mana", "valor": 20, "preco": 100, "classe": "Mago", "descricao": "Aumenta a mana máxima do mago."},
    "Amuleto Elemental": {"efeito": "dano_magico", "valor": 4, "preco": 150, "classe": "Mago", "descricao": "Aumenta o dano de magias elementais."},
    "Amuleto do Arquimago": {"efeito": "regeneracao_mana", "valor": 3, "preco": 200, "classe": "Mago", "descricao": "Regenera mana durante o combate."},
    
    # Amuletos para Arqueiro
    "Amuleto do Caçador": {"efeito": "precisao", "valor": 3, "preco": 100, "classe": "Arqueiro", "descricao": "Aumenta a precisão dos ataques à distância."},
    "Amuleto da Águia": {"efeito": "critico", "valor": 5, "preco": 150, "classe": "Arqueiro", "descricao": "Aumenta a chance de acertos críticos."},
    "Amuleto do Vento": {"efeito": "velocidade", "valor": 4, "preco": 200, "classe": "Arqueiro", "descricao": "Aumenta a velocidade de ataque e movimento."}
}

# Consumíveis disponíveis no jogo
consumiveis = {
    # Poções de Cura
    "Poção de Cura Pequena": {"efeito": "vida", "valor": 20, "preco": 15, "descricao": "Restaura 20 pontos de vida."},
    "Poção de Cura": {"efeito": "vida", "valor": 40, "preco": 30, "descricao": "Restaura 40 pontos de vida."},
    "Poção de Cura Grande": {"efeito": "vida", "valor": 70, "preco": 50, "descricao": "Restaura 70 pontos de vida."},
    "Elixir de Vida": {"efeito": "vida", "valor": 100, "preco": 80, "descricao": "Restaura toda a vida do personagem."},
    
    # Poções de Mana
    "Poção de Mana Pequena": {"efeito": "mana", "valor": 15, "preco": 20, "descricao": "Restaura 15 pontos de mana."},
    "Poção de Mana": {"efeito": "mana", "valor": 30, "preco": 35, "descricao": "Restaura 30 pontos de mana."},
    "Poção de Mana Grande": {"efeito": "mana", "valor": 50, "preco": 55, "descricao": "Restaura 50 pontos de mana."},
    "Elixir Arcano": {"efeito": "mana", "valor": 100, "preco": 90, "descricao": "Restaura toda a mana do personagem."},
    
    # Poções de Buff
    "Poção de Força": {"efeito": "buff", "atributo": "forca", "valor": 3, "duracao": 3, "preco": 35, "descricao": "Aumenta força em 3 por 3 turnos."},
    "Poção de Destreza": {"efeito": "buff", "atributo": "destreza", "valor": 3, "duracao": 3, "preco": 35, "descricao": "Aumenta destreza em 3 por 3 turnos."},
    "Poção de Inteligência": {"efeito": "buff", "atributo": "inteligencia", "valor": 3, "duracao": 3, "preco": 35, "descricao": "Aumenta inteligência em 3 por 3 turnos."},
    "Elixir do Herói": {"efeito": "buff", "atributo": "todos", "valor": 2, "duracao": 5, "preco": 75, "descricao": "Aumenta todos os atributos em 2 por 5 turnos."}
}

# Funções auxiliares para manipulação de itens

def obter_item_por_nome(nome_item):
    """Retorna informações de um item específico pelo nome"""
    if nome_item in armas:
        return armas[nome_item], "arma"
    elif nome_item in armaduras:
        return armaduras[nome_item], "armadura"
    elif nome_item in amuletos:
        return amuletos[nome_item], "amuleto"
    elif nome_item in consumiveis:
        return consumiveis[nome_item], "consumivel"
    else:
        return None, None

def itens_por_classe(classe, tipo_item=None):
    """Retorna uma lista de itens disponíveis para uma classe específica"""
    resultado = []
    
    if tipo_item == "arma" or tipo_item is None:
        for nome, info in armas.items():
            if info["classe"] == classe or info["classe"] == "Qualquer":
                resultado.append((nome, info, "arma"))
    
    if tipo_item == "armadura" or tipo_item is None:
        for nome, info in armaduras.items():
            if info["classe"] == classe or info["classe"] == "Qualquer":
                resultado.append((nome, info, "armadura"))
    
    if tipo_item == "amuleto" or tipo_item is None:
        for nome, info in amuletos.items():
            if info["classe"] == classe or info["classe"] == "Qualquer":
                resultado.append((nome, info, "amuleto"))
    
    if tipo_item == "consumivel" or tipo_item is None:
        for nome, info in consumiveis.items():
            resultado.append((nome, info, "consumivel"))
    
    return resultado

def aplicar_efeito_item(jogador, nome_item):
    """Aplica o efeito de um item consumível ao jogador"""
    item, tipo = obter_item_por_nome(nome_item)
    
    if not item or tipo != "consumivel":
        return False, "Item não encontrado ou não é consumível"
    
    if item["efeito"] == "vida":
        vida_anterior = jogador.vida
        jogador.vida = min(jogador.vida + item["valor"], jogador.vida_maxima)
        return True, f"Recuperou {jogador.vida - vida_anterior} pontos de vida"
    
    elif item["efeito"] == "mana":
        mana_anterior = jogador.mana
        jogador.mana = min(jogador.mana + item["valor"], jogador.mana_maxima)
        return True, f"Recuperou {jogador.mana - mana_anterior} pontos de mana"
    
    elif item["efeito"] == "buff":
        buff = {
            "atributo": item["atributo"],
            "valor": item["valor"],
            "duracao": item["duracao"]
        }
        jogador.aplicar_buff(buff)
        
        if item["atributo"] == "todos":
            return True, f"Recebeu +{item['valor']} em todos os atributos por {item['duracao']} turnos"
        else:
            return True, f"Recebeu +{item['valor']} de {item['atributo']} por {item['duracao']} turnos"
    
    return False, "Efeito de item desconhecido" 