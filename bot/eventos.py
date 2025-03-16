import random
import datetime
import logging

logger = logging.getLogger(__name__)

# Eventos globais do mundo organizados por dia da semana (Segunda a Sexta)
eventos_semanais = {
    0: {  # Segunda-feira - Dia do Guerreiro
        "nome": "Torneio dos Guerreiros",
        "descricao": "O torneio semanal dos guerreiros está acontecendo! Todos os guerreiros recebem +25% de força e os inimigos têm 20% mais vida.",
        "buff": {"tipo": "forca", "classe": "Guerreiro", "valor": 0.25},
        "desafio": {"tipo": "vida_inimigo", "valor": 0.2},
        "recompensa": {"moedas": 100, "exp": 50, "item": "Espada de Prata"},
        "dificuldade": 2  # Escala de 1 a 5
    },
    1: {  # Terça-feira - Dia do Mago
        "nome": "Convergência Arcana",
        "descricao": "As linhas de magia estão particularmente fortes hoje! Magos recebem +30% de dano mágico, mas gastam 15% mais mana.",
        "buff": {"tipo": "dano_magico", "classe": "Mago", "valor": 0.3},
        "desafio": {"tipo": "custo_mana", "valor": 0.15},
        "recompensa": {"moedas": 120, "exp": 60, "item": "Grimório Arcano"},
        "dificuldade": 3  # Escala de 1 a 5
    },
    2: {  # Quarta-feira - Dia do Arqueiro
        "nome": "Desafio de Precisão",
        "descricao": "O mestre arqueiro do reino está testando as habilidades dos aventureiros! Arqueiros recebem +40% de precisão, mas os inimigos se movem mais rápido.",
        "buff": {"tipo": "precisao", "classe": "Arqueiro", "valor": 0.4},
        "desafio": {"tipo": "evasao_inimigo", "valor": 0.2},
        "recompensa": {"moedas": 150, "exp": 70, "item": "Arco Élfico"},
        "dificuldade": 4  # Escala de 1 a 5
    },
    3: {  # Quinta-feira - Caça ao Tesouro (para todos)
        "nome": "Caça ao Tesouro Real",
        "descricao": "O rei escondeu tesouros por todo o reino! Todos ganham +25% de chance de encontrar itens, mas os guardiões dos tesouros são mais fortes.",
        "buff": {"tipo": "encontrar_item", "valor": 0.25},
        "desafio": {"tipo": "ataque_inimigo", "valor": 0.3},
        "recompensa": {"moedas": 200, "exp": 80, "item": "Baú do Tesouro"},
        "dificuldade": 3  # Escala de 1 a 5
    },
    4: {  # Sexta-feira - Grande Batalha (para todos)
        "nome": "Invasão das Trevas",
        "descricao": "Uma força maligna invadiu o reino! Todos recebem +20% em todos os atributos, mas enfrentam inimigos de elite com habilidades especiais.",
        "buff": {"tipo": "todos_atributos", "valor": 0.2},
        "desafio": {"tipo": "inimigos_elite", "valor": 1},
        "recompensa": {"moedas": 300, "exp": 100, "item": "Amuleto Místico"},
        "dificuldade": 5  # Escala de 1 a 5
    }
}

# Variáveis globais para evento atual
evento_atual = None
hora_fim_evento = None
participantes_evento = set()  # Armazena IDs de jogadores que estão participando do evento
vitorias_evento = {}  # Armazena vitórias de cada jogador no evento atual

def iniciar_evento_diario(bot, jogadores, db, logger):
    """Inicia o evento correspondente ao dia da semana atual"""
    global evento_atual, hora_fim_evento, participantes_evento, vitorias_evento
    
    try:
        # Obter dia da semana (0 = segunda, 4 = sexta)
        dia_semana = datetime.datetime.now().weekday()
        
        # Verificar se é dia útil (segunda a sexta)
        if dia_semana <= 4:
            # Selecionar evento do dia
            evento_atual = eventos_semanais[dia_semana]
            
            # Definir hora de término (evento dura até meia-noite)
            agora = datetime.datetime.now()
            fim_dia = datetime.datetime(agora.year, agora.month, agora.day, 23, 59, 59)
            hora_fim_evento = fim_dia
            
            # Reiniciar contadores de participação
            participantes_evento = set()
            vitorias_evento = {}
            
            logger.info(f"Evento diário iniciado: {evento_atual['nome']}, término em {hora_fim_evento}")
            
            # Registrar evento no banco de dados
            try:
                db.registrar_evento_atual(evento_atual['nome'], str(hora_fim_evento))
            except Exception as e:
                logger.error(f"Erro ao registrar evento no banco de dados: {e}")
            
            # Notificar todos os jogadores
            for user_id in jogadores:
                try:
                    mensagem = f"*Evento Diário: {evento_atual['nome']}*\n\n"
                    mensagem += f"{evento_atual['descricao']}\n\n"
                    mensagem += f"*Dificuldade:* {'⭐' * evento_atual['dificuldade']}\n\n"
                    mensagem += f"*Recompensas:*\n"
                    mensagem += f"- {evento_atual['recompensa']['moedas']} moedas\n"
                    mensagem += f"- {evento_atual['recompensa']['exp']} pontos de experiência\n"
                    mensagem += f"- Item: {evento_atual['recompensa']['item']}\n\n"
                    mensagem += f"O evento está ativo até o final do dia! Use o comando /evento para participar."
                    
                    bot.send_message(user_id, mensagem, parse_mode="Markdown")
                except Exception as e:
                    logger.error(f"Erro ao notificar jogador {user_id} sobre evento: {e}")
            
            return True
        else:
            # Final de semana - sem evento
            evento_atual = None
            hora_fim_evento = None
            logger.info("Hoje é final de semana, nenhum evento programado")
            return False
    except Exception as e:
        logger.error(f"Erro ao iniciar evento diário: {e}", exc_info=True)
        return False

def verificar_fim_evento(bot, jogadores, db, logger):
    """Verifica se o evento atual terminou e notifica os jogadores"""
    global evento_atual, hora_fim_evento, participantes_evento, vitorias_evento
    
    try:
        if evento_atual and datetime.datetime.now() >= hora_fim_evento:
            logger.info("Evento diário terminou")
            
            # Distribuir recompensas para participantes que venceram o desafio
            for user_id, vitorias in vitorias_evento.items():
                if user_id in jogadores and vitorias > 0:
                    jogador = jogadores[user_id]
                    
                    # Quanto mais vitórias, mais proporção da recompensa
                    fator = min(1.0, vitorias / 3)  # 3 vitórias = recompensa completa
                    
                    # Calcular recompensas
                    moedas = int(evento_atual['recompensa']['moedas'] * fator)
                    exp = int(evento_atual['recompensa']['exp'] * fator)
                    
                    # Conceder recompensas
                    jogador.moedas += moedas
                    subiu_nivel, _ = jogador.adicionar_experiencia(exp)
                    
                    # Adicionar item se tiver 3 ou mais vitórias
                    if vitorias >= 3:
                        jogador.adicionar_item(evento_atual['recompensa']['item'])
                        item_ganho = evento_atual['recompensa']['item']
                    else:
                        item_ganho = None
                    
                    # Salvar jogador
                    db.salvar_jogador(jogador)
                    
                    # Notificar sobre recompensas
                    mensagem = f"*Recompensas do Evento: {evento_atual['nome']}*\n\n"
                    mensagem += f"Você teve {vitorias} vitórias no evento e recebeu:\n"
                    mensagem += f"- {moedas} moedas 💰\n"
                    mensagem += f"- {exp} pontos de experiência ✨\n"
                    
                    if item_ganho:
                        mensagem += f"- Item: {item_ganho} 🎁\n"
                    
                    if subiu_nivel:
                        mensagem += "\nVocê também subiu de nível! 🆙"
                    
                    try:
                        bot.send_message(user_id, mensagem, parse_mode="Markdown")
                    except Exception as e:
                        logger.error(f"Erro ao enviar recompensa para jogador {user_id}: {e}")
            
            # Notificar fim do evento
            for user_id in jogadores:
                if user_id not in vitorias_evento:
                    try:
                        bot.send_message(user_id, f"O evento *{evento_atual['nome']}* terminou! Infelizmente você não participou desta vez. Tente na próxima!")
                    except Exception as e:
                        logger.error(f"Erro ao notificar jogador {user_id} sobre fim do evento: {e}")
            
            # Limpar dados do evento
            evento_atual = None
            hora_fim_evento = None
            participantes_evento = set()
            vitorias_evento = {}
            
            # Atualizar banco de dados
            try:
                db.finalizar_evento_atual()
            except Exception as e:
                logger.error(f"Erro ao finalizar evento no banco de dados: {e}")
            
            return True
        return False
    except Exception as e:
        logger.error(f"Erro ao verificar fim de evento: {e}", exc_info=True)
        return False

def participar_evento(jogador_id, jogador):
    """Registra a participação de um jogador no evento atual"""
    global participantes_evento
    
    if not evento_atual:
        return False, "Não há evento ativo no momento."
    
    # Verificar se o jogador tem nível suficiente
    nivel_minimo = max(1, evento_atual['dificuldade'])
    if jogador.nivel < nivel_minimo:
        return False, f"Você precisa ser pelo menos nível {nivel_minimo} para participar deste evento."
    
    # Adicionar jogador à lista de participantes
    participantes_evento.add(jogador_id)
    
    # Inicializar contagem de vitórias se necessário
    if jogador_id not in vitorias_evento:
        vitorias_evento[jogador_id] = 0
    
    return True, f"Você está participando do evento *{evento_atual['nome']}*! Vença o desafio para ganhar recompensas."

def registrar_vitoria_evento(jogador_id):
    """Registra uma vitória do jogador no evento atual"""
    global vitorias_evento
    
    if not evento_atual or jogador_id not in participantes_evento:
        return False
    
    # Incrementar número de vitórias
    if jogador_id not in vitorias_evento:
        vitorias_evento[jogador_id] = 1
    else:
        vitorias_evento[jogador_id] += 1
    
    return True

def aplicar_modificador_evento(jogador, inimigo=None):
    """Aplica modificadores do evento atual ao jogador e inimigo"""
    if not evento_atual:
        return
    
    # Aplicar buffs ao jogador
    buff = evento_atual.get("buff", {})
    
    # Verificar se o buff é para uma classe específica
    if "classe" in buff and buff["classe"] != jogador.classe:
        return
    
    # Aplicar buff conforme o tipo
    if buff["tipo"] == "forca":
        valor_bonus = int(jogador.forca * buff["valor"])
        jogador.buffs.append({
            "atributo": "forca",
            "valor": valor_bonus,
            "duracao": 3  # Dura 3 turnos
        })
    elif buff["tipo"] == "dano_magico" and jogador.classe == "Mago":
        jogador.buff_temporario = {
            "tipo": "dano",
            "valor": 1 + buff["valor"],
            "duracao": 3
        }
    elif buff["tipo"] == "precisao" and jogador.classe == "Arqueiro":
        valor_bonus = int(jogador.destreza * buff["valor"])
        jogador.buffs.append({
            "atributo": "destreza",
            "valor": valor_bonus,
            "duracao": 3
        })
    elif buff["tipo"] == "todos_atributos":
        # Aplicar bônus em todos os atributos
        valor_forca = int(jogador.forca * buff["valor"])
        valor_destreza = int(jogador.destreza * buff["valor"])
        valor_inteligencia = int(jogador.inteligencia * buff["valor"])
        
        jogador.buffs.append({
            "atributo": "todos",
            "valor": min(valor_forca, valor_destreza, valor_inteligencia),
            "duracao": 3
        })
    
    # Aplicar desafios ao inimigo se for uma batalha
    if inimigo and "desafio" in evento_atual:
        desafio = evento_atual["desafio"]
        
        if desafio["tipo"] == "vida_inimigo":
            inimigo_vida_bonus = int(inimigo.vida * desafio["valor"])
            inimigo.vida += inimigo_vida_bonus
        elif desafio["tipo"] == "ataque_inimigo":
            inimigo.ataque_min = int(inimigo.ataque_min * (1 + desafio["valor"]))
            inimigo.ataque_max = int(inimigo.ataque_max * (1 + desafio["valor"]))
        elif desafio["tipo"] == "evasao_inimigo":
            # Implementado através de lógica na batalha
            inimigo.evasao = desafio["valor"]
        elif desafio["tipo"] == "inimigos_elite":
            # Adicionar habilidade especial ao inimigo
            inimigo.especial = True
            inimigo.nome = f"Elite {inimigo.nome}"
            inimigo.ataque_max += 5
            inimigo.vida += int(inimigo.vida * 0.3)

def obter_modificador_evento(jogador, tipo, valor_base=0):
    """Calcula modificador com base no evento atual para um jogador"""
    global evento_atual
    
    try:
        # Se não houver evento ativo, retorna valor base
        if not evento_atual:
            return valor_base
        
        buff = evento_atual.get("buff", {})
        modificador = 0
        
        # Verificar tipo do buff
        if buff.get("tipo") == tipo or buff.get("tipo") == "todos_atributos":
            # Verificar se o buff é para uma classe específica
            if "classe" in buff and buff["classe"] != jogador.classe:
                return valor_base
            
            # Aplicar modificador
            modificador = buff.get("valor", 0)
            return valor_base * (1 + modificador)
        
        return valor_base
    except Exception as e:
        logging.error(f"Erro ao calcular modificador de evento: {e}", exc_info=True)
        return valor_base

def esta_ativo_evento():
    """Verifica se há um evento ativo atualmente"""
    global evento_atual
    return evento_atual is not None

def obter_evento_atual():
    """Retorna informações sobre o evento atual"""
    global evento_atual, hora_fim_evento, vitorias_evento
    
    if not evento_atual:
        return None
    
    # Calcular tempo restante
    tempo_restante = hora_fim_evento - datetime.datetime.now()
    horas_restantes = tempo_restante.total_seconds() / 3600
    
    return {
        "evento": evento_atual,
        "tempo_restante": round(horas_restantes, 2),
        "hora_fim": hora_fim_evento.strftime("%H:%M:%S"),
        "participantes": len(participantes_evento),
        "vitorias": vitorias_evento
    }

def obter_progresso_jogador_evento(jogador_id):
    """Retorna o progresso de um jogador no evento atual"""
    global vitorias_evento, participantes_evento
    
    if not esta_ativo_evento():
        return None
    
    esta_participando = jogador_id in participantes_evento
    vitorias = vitorias_evento.get(jogador_id, 0) if esta_participando else 0
    
    return {
        "participando": esta_participando,
        "vitorias": vitorias,
        "objetivo": 3  # Número alvo de vitórias para obter a recompensa completa
    } 