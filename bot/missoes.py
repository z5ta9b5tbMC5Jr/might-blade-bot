import random
import logging
from telebot import types

logger = logging.getLogger(__name__)

# Lista de tipos de missões
MISSOES_BATALHA = [
    {
        "titulo": "Caça aos Goblins",
        "descricao": "Derrote 5 goblins que estão aterrorizando a vila.",
        "tipo": "batalha",
        "inimigo_alvo": "Goblin",
        "quantidade_alvo": 5,
        "recompensa": {
            "moedas": 50,
            "exp": 30,
            "item": None  # 30% de chance de ganhar um item
        }
    },
    {
        "titulo": "Eliminação de Lobos",
        "descricao": "Elimine 3 lobos que atacam os viajantes na estrada.",
        "tipo": "batalha",
        "inimigo_alvo": "Lobo",
        "quantidade_alvo": 3,
        "recompensa": {
            "moedas": 40,
            "exp": 25,
            "item": None  # 30% de chance de ganhar um item
        }
    },
    {
        "titulo": "Ameaça dos Mortos-Vivos",
        "descricao": "Derrote 4 esqueletos no cemitério abandonado.",
        "tipo": "batalha",
        "inimigo_alvo": "Esqueleto",
        "quantidade_alvo": 4,
        "recompensa": {
            "moedas": 60,
            "exp": 40,
            "item": None  # 40% de chance de ganhar um item
        }
    },
    {
        "titulo": "Perigo nas Minas",
        "descricao": "Elimine 2 orcs que tomaram controle das minas.",
        "tipo": "batalha",
        "inimigo_alvo": "Orc",
        "quantidade_alvo": 2,
        "recompensa": {
            "moedas": 70,
            "exp": 45,
            "item": None  # 50% de chance de ganhar um item
        }
    },
    {
        "titulo": "Guardiões Antigos",
        "descricao": "Derrote 2 golens de pedra nas ruínas antigas.",
        "tipo": "batalha",
        "inimigo_alvo": "Golem",
        "quantidade_alvo": 2,
        "recompensa": {
            "moedas": 90,
            "exp": 60,
            "item": None  # 60% de chance de ganhar um item
        }
    }
]

def mostrar_missoes(bot, message, jogadores, db):
    """Mostra as missões disponíveis ou a missão atual do jogador"""
    user_id = message.from_user.id
    if user_id not in jogadores:
        bot.reply_to(message, "Você ainda não iniciou o jogo! Use /start primeiro.")
        return
    
    jogador = jogadores[user_id]
    
    # Verificar se o jogador já tem uma missão ativa
    if hasattr(jogador, 'missao_ativa') and jogador.missao_ativa:
        missao = jogador.missao_ativa
        progresso = f"{missao['progresso']}/{missao['quantidade_alvo']}"
        
        # Verificar se a missão foi concluída
        if missao['progresso'] >= missao['quantidade_alvo']:
            # Criar botão para receber recompensa
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🎁 Receber Recompensa", callback_data="receber_recompensa_missao"))
            
            bot.reply_to(message, 
                f"*Missão Concluída!* 🎯\n\n"
                f"*{missao['titulo']}*\n"
                f"{missao['descricao']}\n\n"
                f"Progresso: {progresso} ✅\n\n"
                f"*Recompensas:*\n"
                f"- {missao['recompensa']['moedas']} moedas 💰\n"
                f"- {missao['recompensa']['exp']} pontos de experiência ✨\n"
                f"- Chance de item especial 🎁\n\n"
                f"Clique no botão abaixo para receber sua recompensa!",
                parse_mode="Markdown",
                reply_markup=markup
            )
        else:
            bot.reply_to(message, 
                f"*Missão Atual:* 🎯\n\n"
                f"*{missao['titulo']}*\n"
                f"{missao['descricao']}\n\n"
                f"Progresso: {progresso}\n\n"
                f"*Recompensas:*\n"
                f"- {missao['recompensa']['moedas']} moedas 💰\n"
                f"- {missao['recompensa']['exp']} pontos de experiência ✨\n"
                f"- Chance de item especial 🎁\n\n"
                f"Continue derrotando {missao['inimigo_alvo']} para completar esta missão!",
                parse_mode="Markdown"
            )
    else:
        # Oferecer nova missão
        nova_missao = gerar_missao(jogador)
        
        # Criar botões para aceitar ou recusar
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("✅ Aceitar", callback_data="aceitar_missao"),
            types.InlineKeyboardButton("❌ Recusar", callback_data="recusar_missao")
        )
        
        bot.reply_to(message, 
            f"*Nova Missão Disponível:* 🎯\n\n"
            f"*{nova_missao['titulo']}*\n"
            f"{nova_missao['descricao']}\n\n"
            f"Objetivo: Derrotar {nova_missao['quantidade_alvo']} {nova_missao['inimigo_alvo']}(s)\n\n"
            f"*Recompensas:*\n"
            f"- {nova_missao['recompensa']['moedas']} moedas 💰\n"
            f"- {nova_missao['recompensa']['exp']} pontos de experiência ✨\n"
            f"- Chance de item especial 🎁\n\n"
            f"Deseja aceitar esta missão?",
            parse_mode="Markdown",
            reply_markup=markup
        )
        
        # Armazenar a missão temporariamente
        jogador.missao_temp = nova_missao

def gerar_missao(jogador):
    """Gera uma missão adequada ao nível do jogador"""
    # Selecionar missões adequadas ao nível do jogador
    nivel = jogador.nivel
    
    # Filtrar missões pelo nível de dificuldade
    missoes_disponiveis = MISSOES_BATALHA
    
    # Selecionar uma missão aleatória
    missao = random.choice(missoes_disponiveis).copy()
    
    # Ajustar dificuldade com base no nível do jogador
    if nivel > 5:
        missao['quantidade_alvo'] = min(missao['quantidade_alvo'] + 1, 10)
        missao['recompensa']['moedas'] = int(missao['recompensa']['moedas'] * 1.5)
        missao['recompensa']['exp'] = int(missao['recompensa']['exp'] * 1.5)
    
    # Adicionar campo de progresso
    missao['progresso'] = 0
    
    return missao

def processar_aceitacao_missao(bot, call, jogadores, db):
    """Processa a aceitação de uma missão pelo jogador"""
    user_id = call.from_user.id
    jogador = jogadores[user_id]
    
    if hasattr(jogador, 'missao_temp'):
        # Definir a missão como ativa
        jogador.missao_ativa = jogador.missao_temp
        delattr(jogador, 'missao_temp')
        
        # Salvar no banco de dados
        db.salvar_jogador(jogador)
        
        # Registrar atividade
        db.registrar_atividade(user_id, "aceitar_missao", {
            "missao": jogador.missao_ativa["titulo"]
        })
        
        # Notificar o jogador
        bot.answer_callback_query(call.id, "Missão aceita! Boa sorte, aventureiro!")
        
        # Editar a mensagem original
        bot.edit_message_text(
            f"*Missão Aceita:* ✅\n\n"
            f"*{jogador.missao_ativa['titulo']}*\n"
            f"{jogador.missao_ativa['descricao']}\n\n"
            f"Objetivo: Derrotar {jogador.missao_ativa['quantidade_alvo']} {jogador.missao_ativa['inimigo_alvo']}(s)\n\n"
            f"Use o comando /batalha para encontrar inimigos e avançar em sua missão!",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode="Markdown"
        )
    else:
        bot.answer_callback_query(call.id, "Erro ao aceitar missão. Tente novamente com /missao")

def processar_recusa_missao(bot, call, jogadores):
    """Processa a recusa de uma missão pelo jogador"""
    user_id = call.from_user.id
    jogador = jogadores[user_id]
    
    if hasattr(jogador, 'missao_temp'):
        missao_recusada = jogador.missao_temp["titulo"]
        delattr(jogador, 'missao_temp')
        
        # Notificar o jogador
        bot.answer_callback_query(call.id, "Missão recusada. Volte quando estiver pronto!")
        
        # Editar a mensagem original
        bot.edit_message_text(
            f"Você recusou a missão *{missao_recusada}*.\n\nUse /missao para ver outras missões disponíveis quando estiver pronto.",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode="Markdown"
        )
    else:
        bot.answer_callback_query(call.id, "Erro ao recusar missão. Tente novamente com /missao")

def processar_recompensa_missao(bot, call, jogadores, db):
    """Processa a entrega de recompensa por missão concluída"""
    user_id = call.from_user.id
    jogador = jogadores[user_id]
    
    if hasattr(jogador, 'missao_ativa') and jogador.missao_ativa and jogador.missao_ativa['progresso'] >= jogador.missao_ativa['quantidade_alvo']:
        missao = jogador.missao_ativa
        
        # Adicionar moedas
        jogador.moedas += missao['recompensa']['moedas']
        
        # Adicionar experiência
        subiu_nivel, msg_nivel = jogador.adicionar_experiencia(missao['recompensa']['exp'])
        
        # Verificar se ganha item (30-60% de chance dependendo da missão)
        item_ganho = None
        chance_item = 0.3 + (0.1 * (missao['recompensa']['moedas'] // 20))  # Quanto maior a recompensa, maior a chance
        
        if random.random() < chance_item:
            # Itens possíveis de recompensa
            itens_possiveis = [
                "Poção de Vida Média",
                "Poção de Mana",
                "Fragmento de Cristal",
                "Pedra de Amolar",
                "Essência Mágica"
            ]
            
            # Adicionar itens raros para missões mais difíceis
            if missao['recompensa']['moedas'] >= 70:
                itens_possiveis.extend([
                    "Poção de Vida Grande",
                    "Pedra Elemental",
                    "Elixir de Atributos"
                ])
            
            item_ganho = random.choice(itens_possiveis)
            jogador.inventario.append(item_ganho)
        
        # Construir mensagem de recompensa
        mensagem = f"*Recompensa de Missão Recebida!* 🎉\n\n"
        mensagem += f"Missão: *{missao['titulo']}*\n\n"
        mensagem += f"*Você recebeu:*\n"
        mensagem += f"- {missao['recompensa']['moedas']} moedas 💰\n"
        mensagem += f"- {missao['recompensa']['exp']} pontos de experiência ✨\n"
        
        if item_ganho:
            mensagem += f"- Item: *{item_ganho}* 🎁\n"
        
        if subiu_nivel:
            mensagem += f"\n*PARABÉNS!* {msg_nivel} 🆙"
        
        # Remover a missão ativa
        delattr(jogador, 'missao_ativa')
        
        # Salvar jogador no banco de dados
        db.salvar_jogador(jogador)
        
        # Registrar atividade
        db.registrar_atividade(user_id, "completar_missao", {
            "missao": missao["titulo"],
            "recompensa_moedas": missao['recompensa']['moedas'],
            "recompensa_exp": missao['recompensa']['exp'],
            "item_recebido": item_ganho
        })
        
        # Notificar o jogador
        bot.answer_callback_query(call.id, "Recompensa recebida!")
        
        # Editar a mensagem original
        bot.edit_message_text(
            mensagem,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode="Markdown"
        )
    else:
        bot.answer_callback_query(call.id, "Erro ao receber recompensa. A missão não está concluída ou não existe.") 