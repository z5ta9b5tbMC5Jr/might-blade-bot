import random
import logging
from telebot import types
from .utils import rate_limit
from .monitoring import monitor_requests
from .errors import CustomError
from .itens import armas, armaduras, amuletos, consumiveis, aplicar_efeito_item, obter_item_por_nome, itens_por_classe
from .eventos import obter_modificador_evento, esta_ativo_evento, obter_evento_atual, participar_evento, obter_progresso_jogador_evento
import datetime

logger = logging.getLogger(__name__)

def registrar_comandos(bot, jogadores, db, logger):
    """Registra todos os comandos do bot e seus handlers"""
    
    # Comando /help
    @bot.message_handler(commands=["help"])
    @rate_limit
    @monitor_requests('help')
    def help_command(message):
        try:
            bot.reply_to(message, "Comandos disponíveis:\n\n"
                                 "/start - Inicia o jogo\n"
                                 "/classe - Escolha sua classe\n"
                                 "/moedas - Veja suas moedas\n"
                                 "/perfil - Veja seu perfil\n"
                                 "/batalha - Inicie uma batalha\n"
                                 "/missao - Receba uma missão\n"
                                 "/loja - Acesse a loja\n"
                                 "/inventario - Veja e use itens do seu inventário\n"
                                 "/evento - Veja o evento atual do mundo (se houver)")
        except Exception as e:
            logger.error(f"Erro no comando help: {str(e)}", exc_info=True)
            bot.reply_to(message, "⚠️ Ocorreu um erro ao exibir ajuda. Por favor, tente novamente mais tarde.")

    # Comando /classe
    @bot.message_handler(commands=["classe"])
    @rate_limit
    @monitor_requests('classe')
    def escolher_classe(message):
        try:
            user_id = message.from_user.id
            if user_id not in jogadores:
                bot.reply_to(message, "Você ainda não iniciou o jogo! Use /start primeiro.")
                return
            
            jogador = jogadores[user_id]
            
            # Verificar se o jogador já escolheu uma classe
            if jogador.classe:
                bot.reply_to(message, f"Você já escolheu ser um *{jogador.classe}*. Não é possível mudar de classe após a escolha inicial.", parse_mode="Markdown")
                return
            
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add("Guerreiro", "Mago", "Arqueiro")
            bot.reply_to(message, "Escolha sua classe:", reply_markup=markup)
            
        except Exception as e:
            logger.error(f"Erro no comando classe: {str(e)}", exc_info=True)
            bot.reply_to(message, "⚠️ Ocorreu um erro ao escolher classe. Por favor, tente novamente mais tarde.")

    # Handler para escolha de classe
    @bot.message_handler(func=lambda msg: msg.text in ["Guerreiro", "Mago", "Arqueiro"])
    @monitor_requests('escolha_classe')
    def receber_classe(message):
        try:
            user_id = message.from_user.id
            if user_id not in jogadores:
                bot.reply_to(message, "Você ainda não iniciou o jogo! Use /start primeiro.")
                return
            
            jogador = jogadores[user_id]
            jogador.classe = message.text
            
            # Aplicar modificações de classe
            if jogador.classe == "Guerreiro":
                jogador.forca += 5
                jogador.habilidades = ["Golpe Poderoso", "Escudo Protetor"]
            elif jogador.classe == "Mago":
                jogador.inteligencia += 5
                jogador.mana += 30
                jogador.mana_maxima += 30
                jogador.habilidades = ["Bola de Fogo", "Escudo Arcano"]
            elif jogador.classe == "Arqueiro":
                jogador.destreza += 5
                jogador.habilidades = ["Disparo Múltiplo", "Tiro Certeiro"]
            
            # Descrições das classes
            descricoes = {
                "Guerreiro": "💪 *Guerreiro*: Forte e resistente, especialista em combate corpo a corpo.",
                "Mago": "🧙 *Mago*: Domina as artes arcanas, capaz de lançar poderosos feitiços.",
                "Arqueiro": "🏹 *Arqueiro*: Ágil e preciso, especialista em ataques à distância."
            }
            
            bot.reply_to(message, f"Classe escolhida: {descricoes[message.text]}\n\nSua jornada começa agora! 🎉", parse_mode="Markdown")
            
            # Salvar jogador no banco de dados
            db.salvar_jogador(jogador)
            
            # Registrar atividade
            db.registrar_atividade(user_id, "escolha_classe", {"classe": jogador.classe})
            
        except Exception as e:
            logger.error(f"Erro ao escolher classe: {str(e)}", exc_info=True)
            bot.reply_to(message, "⚠️ Ocorreu um erro ao escolher classe. Por favor, tente novamente mais tarde.")

    # Comando /moedas
    @bot.message_handler(commands=["moedas"])
    @rate_limit
    @monitor_requests('moedas')
    def ver_moedas(message):
        try:
            user_id = message.from_user.id
            if user_id not in jogadores:
                bot.reply_to(message, "Você ainda não iniciou o jogo! Use /start primeiro.")
                return
            
            bot.reply_to(message, f"Você possui {jogadores[user_id].moedas} moedas 💰")
            
        except Exception as e:
            logger.error(f"Erro no comando moedas: {str(e)}", exc_info=True)
            bot.reply_to(message, "⚠️ Ocorreu um erro ao verificar moedas. Por favor, tente novamente mais tarde.")

    # Comando /perfil
    @bot.message_handler(commands=["perfil"])
    @rate_limit
    @monitor_requests('perfil')
    def ver_perfil(message):
        try:
            user_id = message.from_user.id
            if user_id not in jogadores:
                bot.reply_to(message, "Você ainda não iniciou o jogo! Use /start primeiro.")
                return
            
            jogador = jogadores[user_id]
            classe = jogador.classe if jogador.classe else "Não definida"
            
            perfil = f"*Perfil de {jogador.username}*\n\n"
            perfil += f"🎭 *Classe*: {classe}\n"
            perfil += f"💰 *Moedas*: {jogador.moedas}\n"
            perfil += f"⚔️ *Nível*: {jogador.nivel}\n"
            perfil += f"✨ *Experiência*: {jogador.experiencia}/{jogador.nivel * 20}\n"
            perfil += f"❤️ *Vida*: {jogador.vida}/{jogador.vida_maxima}\n"
            perfil += f"🔮 *Mana*: {jogador.mana}/{jogador.mana_maxima}\n"
            
            # Atributos
            perfil += f"\n💪 *Força*: {jogador.forca}\n"
            perfil += f"🏃 *Destreza*: {jogador.destreza}\n"
            perfil += f"🧠 *Inteligência*: {jogador.inteligencia}\n"
            
            # Equipamentos
            perfil += "\n⚔️ *Equipamentos*:\n"
            if jogador.equipamento["arma"]:
                perfil += f"- Arma: {jogador.equipamento['arma']}\n"
            else:
                perfil += f"- Arma: Nenhuma\n"
                
            if jogador.equipamento["armadura"]:
                perfil += f"- Armadura: {jogador.equipamento['armadura']}\n"
            else:
                perfil += f"- Armadura: Nenhuma\n"
                
            if jogador.equipamento["amuleto"]:
                perfil += f"- Amuleto: {jogador.equipamento['amuleto']}\n"
            else:
                perfil += f"- Amuleto: Nenhum\n"
            
            # Inventário
            if jogador.inventario:
                perfil += "\n🎒 *Inventário*: "
                perfil += f"{len(jogador.inventario)} itens\n"
                
                # Agrupando itens por categoria
                categorias = {}
                for item in jogador.inventario:
                    if item in armas:
                        categoria = "Armas"
                    elif item in armaduras:
                        categoria = "Armaduras"
                    elif item in amuletos:
                        categoria = "Amuletos"
                    elif item in consumiveis:
                        categoria = "Consumíveis"
                    else:
                        categoria = "Outros"
                    
                    if categoria not in categorias:
                        categorias[categoria] = []
                    categorias[categoria].append(item)
                
                # Mostrando número de itens por categoria
                for categoria, itens in categorias.items():
                    perfil += f"- {categoria}: {len(itens)}\n"
            else:
                perfil += "\n🎒 *Inventário*: Vazio"
            
            # Habilidades
            if jogador.habilidades:
                perfil += "\n✨ *Habilidades*:\n"
                for habilidade in jogador.habilidades:
                    perfil += f"- {habilidade}\n"
            
            # Buffs ativos
            if jogador.buffs:
                perfil += "\n⚡ *Buffs Ativos*:\n"
                for buff in jogador.buffs:
                    perfil += f"- {buff['atributo'].capitalize()}: +{buff['valor']} (Turnos restantes: {buff['duracao']})\n"
            
            # Evento atual - se estiver participando
            if esta_ativo_evento():
                progresso = obter_progresso_jogador_evento(user_id)
                if progresso and progresso["participando"]:
                    perfil += f"\n🌟 *Evento Ativo*: {progresso['vitorias']}/{progresso['objetivo']} vitórias\n"
            
            bot.reply_to(message, perfil, parse_mode="Markdown")
            
        except Exception as e:
            logger.error(f"Erro no comando perfil: {str(e)}", exc_info=True)
            bot.reply_to(message, "⚠️ Ocorreu um erro ao exibir perfil. Por favor, tente novamente mais tarde.")

    # Comando /batalha
    @bot.message_handler(commands=["batalha"])
    @rate_limit
    @monitor_requests('batalha')
    def iniciar_batalha(message):
        try:
            user_id = message.from_user.id
            if user_id not in jogadores:
                bot.reply_to(message, "Você ainda não iniciou o jogo! Use /start primeiro.")
                return
                
            jogador = jogadores[user_id]
            
            # Verificar se o jogador já está em uma batalha
            if hasattr(jogador, 'batalha_ativa') and jogador.batalha_ativa:
                bot.reply_to(message, "Você já está em uma batalha! Termine-a antes de iniciar outra.")
                return
            
            # Verificar se o jogador tem vida suficiente
            if jogador.vida < jogador.vida_maxima * 0.3:  # Menos de 30% de vida
                bot.reply_to(message, f"Você está muito ferido para batalhar! Sua vida atual: {jogador.vida}/{jogador.vida_maxima} ❤️\nUse poções de cura ou aguarde para se recuperar.")
                return
            
            # Gerar um inimigo aleatório baseado no nível do jogador
            inimigo = gerar_inimigo(jogador.nivel)
            
            # Criar objeto da batalha
            jogador.batalha_ativa = {
                "inimigo": inimigo,
                "turno": 1
            }
            
            # Aplicar modificadores de evento se houver
            if esta_ativo_evento():
                evento_info = obter_evento_atual()
                if evento_info and "buff" in evento_info["evento"]:
                    buff = evento_info["evento"]["buff"]
                    if buff["tipo"] == "combate":
                        # Aplicar buff de combate (exemplo: aumento de dano)
                        jogador.buff_temporario = {
                            "tipo": "dano",
                            "valor": buff["valor"],
                            "duracao": 3  # Dura 3 turnos
                        }
            
            # Registrar atividade
            db.registrar_atividade(user_id, "iniciar_batalha", {"inimigo": inimigo.nome})
            
            # Exibir informações do inimigo e opções de batalha
            mensagem = f"*Você encontrou um {inimigo.nome} (Nível {inimigo.nivel})!* ⚔️\n\n"
            mensagem += f"{inimigo.descricao}\n\n"
            mensagem += f"Vida do inimigo: {inimigo.vida} ❤️\n"
            mensagem += f"Sua vida: {jogador.vida}/{jogador.vida_maxima} ❤️\n"
            mensagem += f"Sua mana: {jogador.mana}/{jogador.mana_maxima} 🔮\n\n"
            mensagem += "O que você deseja fazer?"
            
            # Criar teclado inline com opções de batalha
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(
                types.InlineKeyboardButton("⚔️ Atacar", callback_data="batalha_atacar"),
                types.InlineKeyboardButton("🏃 Fugir", callback_data="batalha_fugir")
            )
            
            # Adicionar botões de habilidades conforme a classe
            if jogador.classe and jogador.mana >= 10:
                habilidades = obter_habilidades_classe(jogador.classe)
                habilidade_botoes = []
                for hab in habilidades[:2]:  # Limitar a 2 habilidades para não sobrecarregar
                    habilidade_botoes.append(
                        types.InlineKeyboardButton(f"✨ {hab['nome']}", callback_data=f"batalha_habilidade_{hab['id']}")
                    )
                markup.add(*habilidade_botoes)
            
            # Enviar mensagem com as opções
            bot.reply_to(message, mensagem, parse_mode="Markdown", reply_markup=markup)
            
            # Salvar jogador
            db.salvar_jogador(jogador)
            
        except Exception as e:
            logger.error(f"Erro no comando batalha: {str(e)}", exc_info=True)
            bot.reply_to(message, "⚠️ Ocorreu um erro ao iniciar a batalha. Por favor, tente novamente mais tarde.")

    # Handlers para ações de batalha
    @bot.callback_query_handler(func=lambda call: call.data.startswith('batalha_'))
    def callback_batalha(call):
        try:
            user_id = call.from_user.id
            if user_id not in jogadores:
                bot.answer_callback_query(call.id, "Você ainda não iniciou o jogo! Use /start primeiro.")
                return
                
            jogador = jogadores[user_id]
            
            # Verificar se o jogador está em uma batalha
            if not hasattr(jogador, 'batalha_ativa') or not jogador.batalha_ativa:
                bot.answer_callback_query(call.id, "Você não está em uma batalha no momento.")
                return
            
            # Extrair ação da callback data
            acao = call.data.split('_')[1]
            
            # Referenciar o inimigo da batalha atual
            inimigo = jogador.batalha_ativa["inimigo"]
            
            # Processar a ação escolhida
            if acao == "atacar":
                # Calcular dano baseado no ataque do jogador e possíveis equipamentos
                dano_base = random.randint(3, 7)
                dano_bonus = 0
                
                # Adicionar bônus de equipamento
                if hasattr(jogador, 'equipamentos') and jogador.equipamentos:
                    if 'arma' in jogador.equipamentos and jogador.equipamentos['arma']:
                        item = jogador.equipamentos['arma']
                        if isinstance(item, dict) and 'valor' in item:
                            dano_bonus += item['valor']
                
                # Aplicar modificadores de evento ou buffs temporários
                if hasattr(jogador, 'buff_temporario') and jogador.buff_temporario:
                    if jogador.buff_temporario["tipo"] == "dano":
                        dano_base = int(dano_base * jogador.buff_temporario["valor"])
                        jogador.buff_temporario["duracao"] -= 1
                        if jogador.buff_temporario["duracao"] <= 0:
                            delattr(jogador, 'buff_temporario')
                
                # Calcular dano final
                dano_total = dano_base + dano_bonus
                
                # Aplicar dano ao inimigo
                inimigo.vida -= dano_total
                
                # Verificar resultado da batalha
                if inimigo.vida <= 0:
                    # Inimigo derrotado, finalizar batalha
                    _processar_resultado_batalha(call.message, jogador, inimigo, db)
                    delattr(jogador, 'batalha_ativa')
                else:
                    # Inimigo sobrevive, contra-ataca
                    dano_inimigo = random.randint(inimigo.ataque_min, inimigo.ataque_max)
                    
                    # Reduzir dano com base na defesa do jogador
                    defesa_bonus = 0
                    if hasattr(jogador, 'equipamentos') and jogador.equipamentos:
                        if 'armadura' in jogador.equipamentos and jogador.equipamentos['armadura']:
                            item = jogador.equipamentos['armadura']
                            if isinstance(item, dict) and 'valor' in item:
                                defesa_bonus += item['valor']
                    
                    dano_reduzido = max(1, dano_inimigo - defesa_bonus)
                    jogador.vida -= dano_reduzido
                    
                    # Verificar se o jogador foi derrotado
                    if jogador.vida <= 0:
                        # Jogador derrotado, finalizar batalha
                        _processar_resultado_batalha(call.message, jogador, inimigo, db)
                        delattr(jogador, 'batalha_ativa')
                    else:
                        # Batalha continua, atualizar mensagem
                        jogador.batalha_ativa["turno"] += 1
                        
                        # Recuperar um pouco de mana a cada turno
                        jogador.mana = min(jogador.mana_maxima, jogador.mana + 2)
                        
                        mensagem = f"*Turno {jogador.batalha_ativa['turno']}*\n\n"
                        mensagem += f"Você atacou o *{inimigo.nome}* e causou *{dano_total}* de dano! ⚔️\n"
                        mensagem += f"O *{inimigo.nome}* contra-atacou e causou *{dano_reduzido}* de dano! 🗡️\n\n"
                        mensagem += f"Vida do {inimigo.nome}: {inimigo.vida} ❤️\n"
                        mensagem += f"Sua vida: {jogador.vida}/{jogador.vida_maxima} ❤️\n"
                        mensagem += f"Sua mana: {jogador.mana}/{jogador.mana_maxima} 🔮\n\n"
                        mensagem += "O que você deseja fazer agora?"
                        
                        # Atualizar teclado inline com opções
                        markup = types.InlineKeyboardMarkup(row_width=2)
                        markup.add(
                            types.InlineKeyboardButton("⚔️ Atacar", callback_data="batalha_atacar"),
                            types.InlineKeyboardButton("🏃 Fugir", callback_data="batalha_fugir")
                        )
                        
                        # Adicionar botões de habilidades conforme a classe e mana disponível
                        if jogador.classe and jogador.mana >= 10:
                            habilidades = obter_habilidades_classe(jogador.classe)
                            habilidade_botoes = []
                            for hab in habilidades[:2]:  # Limitar a 2 habilidades
                                habilidade_botoes.append(
                                    types.InlineKeyboardButton(f"✨ {hab['nome']}", callback_data=f"batalha_habilidade_{hab['id']}")
                                )
                            markup.add(*habilidade_botoes)
                        
                        # Atualizar mensagem com novas informações
                        bot.edit_message_text(text=mensagem, 
                                            chat_id=call.message.chat.id, 
                                            message_id=call.message.message_id,
                                            parse_mode="Markdown",
                                            reply_markup=markup)
                        
                        bot.answer_callback_query(call.id, f"Você causou {dano_total} de dano ao inimigo!")
            
            elif acao == "fugir":
                # Tentar fugir com 70% de chance de sucesso
                if random.random() < 0.7:
                    # Fuga bem sucedida
                    mensagem = f"Você conseguiu fugir do *{inimigo.nome}*! 🏃💨\n"
                    mensagem += "Você retornou para a segurança da cidade."
                    
                    bot.edit_message_text(text=mensagem, 
                                        chat_id=call.message.chat.id, 
                                        message_id=call.message.message_id,
                                        parse_mode="Markdown")
                    
                    # Remover batalha ativa
                    delattr(jogador, 'batalha_ativa')
                    
                    # Registrar atividade
                    db.registrar_atividade(user_id, "fugir_batalha", {"inimigo": inimigo.nome, "sucesso": True})
                    
                    bot.answer_callback_query(call.id, "Você conseguiu fugir com sucesso!")
                else:
                    # Fuga falhou
                    mensagem = f"Você tentou fugir, mas o *{inimigo.nome}* te alcançou! 🏃❌\n\n"
                    
                    # Inimigo ataca devido à falha na fuga
                    dano_inimigo = random.randint(inimigo.ataque_min, inimigo.ataque_max)
                    
                    # Reduzir dano com base na defesa do jogador
                    defesa_bonus = 0
                    if hasattr(jogador, 'equipamentos') and jogador.equipamentos:
                        if 'armadura' in jogador.equipamentos and jogador.equipamentos['armadura']:
                            item = jogador.equipamentos['armadura']
                            if isinstance(item, dict) and 'valor' in item:
                                defesa_bonus += item['valor']
                    
                    dano_reduzido = max(1, dano_inimigo - defesa_bonus)
                    jogador.vida -= dano_reduzido
                    
                    mensagem += f"O *{inimigo.nome}* te ataca e causa *{dano_reduzido}* de dano! 🗡️\n\n"
                    
                    # Verificar se o jogador foi derrotado
                    if jogador.vida <= 0:
                        # Jogador derrotado, finalizar batalha
                        _processar_resultado_batalha(call.message, jogador, inimigo, db)
                        delattr(jogador, 'batalha_ativa')
                    else:
                        # Batalha continua
                        jogador.batalha_ativa["turno"] += 1
                        
                        # Recuperar um pouco de mana a cada turno
                        jogador.mana = min(jogador.mana_maxima, jogador.mana + 2)
                        
                        mensagem += f"Vida do {inimigo.nome}: {inimigo.vida} ❤️\n"
                        mensagem += f"Sua vida: {jogador.vida}/{jogador.vida_maxima} ❤️\n"
                        mensagem += f"Sua mana: {jogador.mana}/{jogador.mana_maxima} 🔮\n\n"
                        mensagem += "O que você deseja fazer agora?"
                        
                        # Atualizar teclado inline com opções
                        markup = types.InlineKeyboardMarkup(row_width=2)
                        markup.add(
                            types.InlineKeyboardButton("⚔️ Atacar", callback_data="batalha_atacar"),
                            types.InlineKeyboardButton("🏃 Fugir", callback_data="batalha_fugir")
                        )
                        
                        # Adicionar botões de habilidades conforme a classe e mana disponível
                        if jogador.classe and jogador.mana >= 10:
                            habilidades = obter_habilidades_classe(jogador.classe)
                            habilidade_botoes = []
                            for hab in habilidades[:2]:  # Limitar a 2 habilidades
                                habilidade_botoes.append(
                                    types.InlineKeyboardButton(f"✨ {hab['nome']}", callback_data=f"batalha_habilidade_{hab['id']}")
                                )
                            markup.add(*habilidade_botoes)
                        
                        # Atualizar mensagem com novas informações
                        bot.edit_message_text(text=mensagem, 
                                            chat_id=call.message.chat.id, 
                                            message_id=call.message.message_id,
                                            parse_mode="Markdown",
                                            reply_markup=markup)
                    
                    # Registrar atividade
                    db.registrar_atividade(user_id, "fugir_batalha", {"inimigo": inimigo.nome, "sucesso": False})
                    
                    bot.answer_callback_query(call.id, "Você falhou em fugir!")
            
            elif acao.startswith("habilidade"):
                # Usar habilidade
                habilidade_id = call.data.split('_')[2]
                
                # Obter habilidade
                habilidade = None
                habilidades = obter_habilidades_classe(jogador.classe)
                for hab in habilidades:
                    if hab['id'] == habilidade_id:
                        habilidade = hab
                        break
                
                if not habilidade:
                    bot.answer_callback_query(call.id, "Habilidade não encontrada!")
                    return
                
                # Verificar se tem mana suficiente
                custo_mana = habilidade.get('custo_mana', 10)
                if jogador.mana < custo_mana:
                    bot.answer_callback_query(call.id, f"Mana insuficiente! Você precisa de {custo_mana} mana.")
                    return
                
                # Reduzir mana
                jogador.mana -= custo_mana
                
                # Calcular dano da habilidade
                dano_base = habilidade.get('dano_base', 10)
                multiplicador = habilidade.get('multiplicador', 1.5)
                
                # Dano depende da classe
                if jogador.classe == "Guerreiro":
                    # Guerreiros usam força
                    dano_atributo = jogador.forca if hasattr(jogador, 'forca') else 5
                elif jogador.classe == "Mago":
                    # Magos usam inteligência
                    dano_atributo = jogador.inteligencia if hasattr(jogador, 'inteligencia') else 5
                elif jogador.classe == "Arqueiro":
                    # Arqueiros usam agilidade
                    dano_atributo = jogador.agilidade if hasattr(jogador, 'agilidade') else 5
                else:
                    dano_atributo = 5
                
                # Calcular dano final
                dano_total = int((dano_base + dano_atributo) * multiplicador)
                
                # Aplicar modificadores de evento se houver
                if esta_ativo_evento():
                    evento_info = obter_evento_atual()
                    if evento_info and "buff" in evento_info["evento"]:
                        buff = evento_info["evento"]["buff"]
                        if buff["tipo"] == "magico" and jogador.classe == "Mago":
                            dano_total = int(dano_total * buff["valor"])
                        elif buff["tipo"] == "fisico" and jogador.classe in ["Guerreiro", "Arqueiro"]:
                            dano_total = int(dano_total * buff["valor"])
                
                # Aplicar dano ao inimigo
                inimigo.vida -= dano_total
                
                # Verificar resultado da batalha
                if inimigo.vida <= 0:
                    # Inimigo derrotado, finalizar batalha
                    _processar_resultado_batalha(call.message, jogador, inimigo, db)
                    delattr(jogador, 'batalha_ativa')
                else:
                    # Inimigo sobrevive, contra-ataca
                    dano_inimigo = random.randint(inimigo.ataque_min, inimigo.ataque_max)
                    
                    # Reduzir dano com base na defesa do jogador
                    defesa_bonus = 0
                    if hasattr(jogador, 'equipamentos') and jogador.equipamentos:
                        if 'armadura' in jogador.equipamentos and jogador.equipamentos['armadura']:
                            item = jogador.equipamentos['armadura']
                            if isinstance(item, dict) and 'valor' in item:
                                defesa_bonus += item['valor']
                    
                    dano_reduzido = max(1, dano_inimigo - defesa_bonus)
                    jogador.vida -= dano_reduzido
                    
                    # Verificar se o jogador foi derrotado
                    if jogador.vida <= 0:
                        # Jogador derrotado, finalizar batalha
                        _processar_resultado_batalha(call.message, jogador, inimigo, db)
                        delattr(jogador, 'batalha_ativa')
                    else:
                        # Batalha continua, atualizar mensagem
                        jogador.batalha_ativa["turno"] += 1
                        
                        mensagem = f"*Turno {jogador.batalha_ativa['turno']}*\n\n"
                        mensagem += f"Você usou *{habilidade['nome']}* e causou *{dano_total}* de dano! ✨\n"
                        if 'efeito' in habilidade and habilidade['efeito']:
                            mensagem += f"*Efeito:* {habilidade['efeito']}\n"
                        mensagem += f"O *{inimigo.nome}* contra-atacou e causou *{dano_reduzido}* de dano! 🗡️\n\n"
                        mensagem += f"Vida do {inimigo.nome}: {inimigo.vida} ❤️\n"
                        mensagem += f"Sua vida: {jogador.vida}/{jogador.vida_maxima} ❤️\n"
                        mensagem += f"Sua mana: {jogador.mana}/{jogador.mana_maxima} 🔮\n\n"
                        mensagem += "O que você deseja fazer agora?"
                        
                        # Atualizar teclado inline com opções
                        markup = types.InlineKeyboardMarkup(row_width=2)
                        markup.add(
                            types.InlineKeyboardButton("⚔️ Atacar", callback_data="batalha_atacar"),
                            types.InlineKeyboardButton("🏃 Fugir", callback_data="batalha_fugir")
                        )
                        
                        # Adicionar botões de habilidades conforme a classe e mana disponível
                        if jogador.classe and jogador.mana >= 10:
                            habilidades = obter_habilidades_classe(jogador.classe)
                            habilidade_botoes = []
                            for hab in habilidades[:2]:  # Limitar a 2 habilidades
                                habilidade_botoes.append(
                                    types.InlineKeyboardButton(f"✨ {hab['nome']}", callback_data=f"batalha_habilidade_{hab['id']}")
                                )
                            markup.add(*habilidade_botoes)
                        
                        # Atualizar mensagem com novas informações
                        bot.edit_message_text(text=mensagem, 
                                            chat_id=call.message.chat.id, 
                                            message_id=call.message.message_id,
                                            parse_mode="Markdown",
                                            reply_markup=markup)
                        
                        bot.answer_callback_query(call.id, f"Você usou {habilidade['nome']} e causou {dano_total} de dano!")
            
            # Salvar o jogador
            db.salvar_jogador(jogador)
            
        except Exception as e:
            logger.error(f"Erro no callback de batalha: {str(e)}", exc_info=True)
            bot.answer_callback_query(call.id, "⚠️ Ocorreu um erro ao processar a ação de batalha.")
    
    # Função para gerar inimigo baseado no nível do jogador
    def gerar_inimigo(nivel_jogador):
        # Lista de inimigos possíveis por faixa de nível
        inimigos_nivel1 = [
            {"nome": "Slime", "nivel": 1, "vida": 15, "ataque_min": 2, "ataque_max": 5, "moedas_drop": 10, "exp_drop": 8, 
            "descricao": "Uma criatura gelatinosa e viscosa que se move lentamente."},
            
            {"nome": "Rato Gigante", "nivel": 1, "vida": 12, "ataque_min": 3, "ataque_max": 6, "moedas_drop": 8, "exp_drop": 7, 
            "descricao": "Um rato de tamanho anormal com dentes afiados e olhos vermelhos."},
            
            {"nome": "Kobold", "nivel": 1, "vida": 18, "ataque_min": 2, "ataque_max": 4, "moedas_drop": 12, "exp_drop": 9, 
            "descricao": "Uma pequena criatura reptiliana que adora armadilhas e emboscadas."}
        ]
        
        inimigos_nivel2 = [
            {"nome": "Lobo", "nivel": 2, "vida": 25, "ataque_min": 4, "ataque_max": 8, "moedas_drop": 15, "exp_drop": 12, 
            "descricao": "Um lobo feroz com pelagem negra e olhos brilhantes."},
            
            {"nome": "Goblin", "nivel": 2, "vida": 22, "ataque_min": 3, "ataque_max": 7, "moedas_drop": 18, "exp_drop": 14, 
            "descricao": "Uma criatura verde de pequeno porte, ágil e traiçoeira."},
            
            {"nome": "Esqueleto", "nivel": 2, "vida": 20, "ataque_min": 5, "ataque_max": 9, "moedas_drop": 20, "exp_drop": 15, 
            "descricao": "Restos mortais animados por magia negra, carregando ossos como armas."}
        ]
        
        inimigos_nivel3 = [
            {"nome": "Orc", "nivel": 3, "vida": 35, "ataque_min": 6, "ataque_max": 12, "moedas_drop": 25, "exp_drop": 20, 
            "descricao": "Uma criatura musculosa com presas proeminentes e pele verde escura."},
            
            {"nome": "Bandido", "nivel": 3, "vida": 30, "ataque_min": 5, "ataque_max": 10, "moedas_drop": 30, "exp_drop": 18, 
            "descricao": "Um ladrão armado que ataca viajantes na estrada."},
            
            {"nome": "Harpia", "nivel": 3, "vida": 28, "ataque_min": 7, "ataque_max": 11, "moedas_drop": 28, "exp_drop": 22, 
            "descricao": "Uma criatura com corpo de pássaro e cabeça de mulher, com garras afiadas."}
        ]
        
        inimigos_nivel4 = [
            {"nome": "Golem de Pedra", "nivel": 4, "vida": 50, "ataque_min": 8, "ataque_max": 15, "moedas_drop": 40, "exp_drop": 30, 
            "descricao": "Uma estátua animada feita de pedra maciça, lenta mas poderosa."},
            
            {"nome": "Espectro", "nivel": 4, "vida": 40, "ataque_min": 10, "ataque_max": 18, "moedas_drop": 45, "exp_drop": 35, 
            "descricao": "Uma entidade fantasmagórica que sussurra horrores enquanto ataca."},
            
            {"nome": "Ogro", "nivel": 4, "vida": 60, "ataque_min": 12, "ataque_max": 20, "moedas_drop": 50, "exp_drop": 40, 
            "descricao": "Um gigante brutamontes que carrega um grande porrete de madeira."}
        ]
        
        inimigos_nivel5 = [
            {"nome": "Troll", "nivel": 5, "vida": 80, "ataque_min": 15, "ataque_max": 25, "moedas_drop": 70, "exp_drop": 55, 
            "descricao": "Uma criatura enorme com pele grossa e capacidade de regeneração."},
            
            {"nome": "Minotauro", "nivel": 5, "vida": 75, "ataque_min": 18, "ataque_max": 28, "moedas_drop": 80, "exp_drop": 60, 
            "descricao": "Um ser com corpo de homem e cabeça de touro, empunhando um machado de guerra."},
            
            {"nome": "Elemental de Fogo", "nivel": 5, "vida": 70, "ataque_min": 20, "ataque_max": 30, "moedas_drop": 85, "exp_drop": 65, 
            "descricao": "Uma entidade composta de chamas vivas, que queima tudo em seu caminho."}
        ]
        
        # Selecionar inimigo com base no nível do jogador
        if nivel_jogador <= 2:
            return random.choice(inimigos_nivel1)
        elif nivel_jogador <= 5:
            return random.choice(inimigos_nivel2)
        elif nivel_jogador <= 8:
            return random.choice(inimigos_nivel3)
        elif nivel_jogador <= 10:
            return random.choice(inimigos_nivel4)
        else:
            return random.choice(inimigos_nivel5)

    # Comando /evento
    @bot.message_handler(commands=["evento"])
    @rate_limit
    @monitor_requests('evento')
    def ver_evento(message):
        try:
            user_id = message.from_user.id
            # Importar funções necessárias do módulo eventos
            from .eventos import (
                esta_ativo_evento, 
                obter_evento_atual, 
                participar_evento, 
                obter_progresso_jogador_evento
            )
            
            if not esta_ativo_evento():
                # Verificar o dia da semana para informar o próximo evento
                dia_semana = datetime.datetime.now().weekday()
                
                if dia_semana >= 5:  # Final de semana
                    proximo_evento = "segunda-feira"
                else:
                    proximo_evento = "amanhã"
                
                bot.reply_to(
                    message, 
                    f"Não há nenhum evento global ativo no momento. O próximo evento será {proximo_evento}.",
                    parse_mode="Markdown"
                )
                return
            
            # Verificar se o usuário já iniciou o jogo
            if user_id not in jogadores:
                bot.reply_to(message, "Você ainda não iniciou o jogo! Use /start primeiro.")
                return
            
            jogador = jogadores[user_id]
            
            # Verificar se o jogador está tentando participar do evento
            args = message.text.split()
            if len(args) > 1 and args[1].lower() == "participar":
                # Tentar participar do evento
                sucesso, mensagem = participar_evento(user_id, jogador)
                bot.reply_to(message, mensagem, parse_mode="Markdown")
                
                # Salvar jogador no banco de dados
                if sucesso:
                    db.salvar_jogador(jogador)
                    # Registrar atividade
                    evento_atual = obter_evento_atual()
                    db.registrar_atividade(user_id, "participar_evento", {
                        "evento": evento_atual["evento"]["nome"]
                    })
                return
            
            # Obter informações do evento atual
            evento_info = obter_evento_atual()
            if not evento_info:
                bot.reply_to(message, "Não foi possível obter informações sobre o evento atual.")
                return
            
            # Obter progresso do jogador no evento
            progresso = obter_progresso_jogador_evento(user_id)
            
            # Construir mensagem do evento
            mensagem = f"*Evento Diário: {evento_info['evento']['nome']}*\n\n"
            mensagem += f"{evento_info['evento']['descricao']}\n\n"
            mensagem += f"*Dificuldade:* {'⭐' * evento_info['evento']['dificuldade']}\n\n"
            
            # Informações de tempo
            mensagem += f"⏳ Tempo restante: {evento_info['tempo_restante']:.1f} horas\n"
            mensagem += f"⏰ Termina às: {evento_info['hora_fim']}\n\n"
            
            # Recompensas
            mensagem += f"*Recompensas:*\n"
            mensagem += f"- {evento_info['evento']['recompensa']['moedas']} moedas\n"
            mensagem += f"- {evento_info['evento']['recompensa']['exp']} pontos de experiência\n"
            mensagem += f"- Item: {evento_info['evento']['recompensa']['item']}\n\n"
            
            # Informações de participação
            mensagem += f"👥 Participantes: {evento_info['participantes']}\n\n"
            
            # Status do jogador
            if progresso and progresso["participando"]:
                mensagem += f"*Seu Progresso:* {progresso['vitorias']}/{progresso['objetivo']} vitórias\n"
                if progresso['vitorias'] < progresso['objetivo']:
                    mensagem += "Continue participando de batalhas para completar o evento!\n"
                else:
                    mensagem += "Você atingiu o objetivo! Continue até o fim do evento para garantir suas recompensas.\n"
            else:
                mensagem += "*Você ainda não está participando deste evento!*\n"
                mensagem += "Use o comando `/evento participar` para se juntar ao evento e ganhar recompensas.\n"
            
            # Criar botão para participar se ainda não estiver participando
            markup = None
            if not (progresso and progresso["participando"]):
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("✅ Participar do Evento", callback_data="participar_evento"))
            
            bot.reply_to(message, mensagem, parse_mode="Markdown", reply_markup=markup)
            
        except Exception as e:
            logger.error(f"Erro no comando evento: {str(e)}", exc_info=True)
            bot.reply_to(message, "⚠️ Ocorreu um erro ao verificar eventos. Por favor, tente novamente mais tarde.")

    # Handler para participação em eventos via botão inline
    @bot.callback_query_handler(func=lambda call: call.data == "participar_evento")
    def callback_participar_evento(call):
        try:
            user_id = call.from_user.id
            if user_id not in jogadores:
                bot.answer_callback_query(call.id, "Você ainda não iniciou o jogo! Use /start primeiro.")
                return
            
            jogador = jogadores[user_id]
            
            # Importar função para participar do evento
            from .eventos import participar_evento, esta_ativo_evento
            
            if not esta_ativo_evento():
                bot.answer_callback_query(call.id, "Não há evento ativo no momento.")
                return
            
            # Tentar participar do evento
            sucesso, mensagem = participar_evento(user_id, jogador)
            
            # Salvar jogador no banco de dados
            if sucesso:
                db.salvar_jogador(jogador)
                
                # Registrar atividade
                from .eventos import obter_evento_atual, obter_progresso_jogador_evento
                evento_atual = obter_evento_atual()
                db.registrar_atividade(user_id, "participar_evento", {
                    "evento": evento_atual["evento"]["nome"]
                })
            
            bot.answer_callback_query(call.id, mensagem)
            
            # Atualizar mensagem original
            evento_info = obter_evento_atual()
            progresso = obter_progresso_jogador_evento(user_id)
            
            # Construir mensagem atualizada
            mensagem = f"*Evento Diário: {evento_info['evento']['nome']}*\n\n"
            mensagem += f"{evento_info['evento']['descricao']}\n\n"
            mensagem += f"*Dificuldade:* {'⭐' * evento_info['evento']['dificuldade']}\n\n"
            
            # Informações de tempo
            mensagem += f"⏳ Tempo restante: {evento_info['tempo_restante']:.1f} horas\n"
            mensagem += f"⏰ Termina às: {evento_info['hora_fim']}\n\n"
            
            # Recompensas
            mensagem += f"*Recompensas:*\n"
            mensagem += f"- {evento_info['evento']['recompensa']['moedas']} moedas\n"
            mensagem += f"- {evento_info['evento']['recompensa']['exp']} pontos de experiência\n"
            mensagem += f"- Item: {evento_info['evento']['recompensa']['item']}\n\n"
            
            # Informações de participação
            mensagem += f"👥 Participantes: {evento_info['participantes']}\n\n"
            
            # Status do jogador (agora está participando)
            mensagem += f"*Seu Progresso:* {progresso['vitorias']}/{progresso['objetivo']} vitórias\n"
            mensagem += "Participe de batalhas para completar o evento!\n"
            
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=mensagem,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            logger.error(f"Erro no callback de participação em evento: {str(e)}", exc_info=True)
            bot.answer_callback_query(call.id, "⚠️ Ocorreu um erro ao participar do evento.")

    # Funções auxiliares para eventos
    def esta_ativo_evento():
        # Usar a implementação real do módulo eventos
        from .eventos import esta_ativo_evento as check_evento
        return check_evento()
    
    def obter_evento_atual():
        # Usar a implementação real do módulo eventos
        from .eventos import obter_evento_atual as get_evento
        return get_evento()
    
    # Função auxiliar para processar resultado de batalha
    def _processar_resultado_batalha(message, jogador, inimigo, db):
        # Verificar se o jogador ou o inimigo foi derrotado
        if jogador.vida <= 0:
            bot.reply_to(message, f"Você foi derrotado pelo *{inimigo.nome}*! 💀\nPerdeu *{inimigo.moedas_drop // 2}* moedas e retornou para a cidade para se recuperar.", parse_mode="Markdown")
            jogador.vida = jogador.vida_maxima // 2  # Recupera metade da vida
            jogador.moedas = max(0, jogador.moedas - (inimigo.moedas_drop // 2))  # Perde moedas
            
            # Registrar atividade
            db.registrar_atividade(message.from_user.id, "derrota_batalha", {
                "inimigo": inimigo.nome,
                "nivel_inimigo": inimigo.nivel,
                "moedas_perdidas": inimigo.moedas_drop // 2
            })
            
        elif inimigo.vida <= 0:
            # Calcular recompensas
            moedas_ganhas = inimigo.moedas_drop
            exp_ganha = inimigo.exp_drop
            
            # Verificar participação em evento
            from .eventos import (
                esta_ativo_evento, 
                obter_evento_atual, 
                registrar_vitoria_evento, 
                obter_progresso_jogador_evento
            )
            
            # Verificar se há evento de recompensa ativo
            if esta_ativo_evento():
                evento_info = obter_evento_atual()
                user_id = message.from_user.id
                
                if evento_info:
                    # Verificar participação do jogador no evento
                    progresso = obter_progresso_jogador_evento(user_id)
                    
                    if progresso and progresso["participando"]:
                        # Registrar vitória no evento
                        registrou = registrar_vitoria_evento(user_id)
                        
                        if registrou:
                            # Atualizar evento no banco de dados
                            evento_db = db.obter_evento_ativo()
                            if evento_db:
                                db.registrar_vitoria_evento(user_id, evento_db["id"])
                        
                        # Aplicar modificador de recompensa do evento
                        buff = evento_info["evento"].get("buff", {})
                        if buff.get("tipo") == "recompensa":
                            multiplier = buff.get("valor", 0)
                            moedas_ganhas = int(moedas_ganhas * (1 + multiplier))
                            exp_ganha = int(exp_ganha * (1 + multiplier))
                        
                        # Mensagem de progresso do evento
                        progresso_atualizado = obter_progresso_jogador_evento(user_id)
                        if progresso_atualizado:
                            vitorias = progresso_atualizado["vitorias"]
                            objetivo = progresso_atualizado["objetivo"]
                            
                            mensagem_evento = f"\n\n🌟 *Evento: {evento_info['evento']['nome']}*\n"
                            mensagem_evento += f"Você tem {vitorias}/{objetivo} vitórias no evento!"
                            if vitorias >= objetivo:
                                mensagem_evento += "\nVocê atingiu o objetivo do evento! Continue até o fim do evento para receber recompensas extras."
            
            # Adicionar recompensas ao jogador
            jogador.moedas += moedas_ganhas
            subiu_nivel, msg_nivel = jogador.adicionar_experiencia(exp_ganha)
            
            # Gerar mensagem de vitória
            mensagem = f"Você derrotou o *{inimigo.nome}*! 🎉\n\n"
            mensagem += f"*Recompensas:*\n"
            mensagem += f"💰 {moedas_ganhas} moedas\n"
            mensagem += f"✨ {exp_ganha} pontos de experiência\n"
            
            # Verificar se o inimigo dropou um item
            item_drop = None
            chance_drop = random.random()
            
            # Aumentar chance de drop se estiver participando de evento
            if esta_ativo_evento() and progresso and progresso["participando"]:
                chance_drop += 0.1  # +10% de chance para participantes de eventos
            
            if chance_drop < 0.2:  # 20% de chance base
                # Lista de possíveis itens por tipo de inimigo
                itens_comuns = ["Poção de Vida Pequena", "Pedra de Amolar", "Bandagem"]
                itens_medios = ["Poção de Vida Média", "Poção de Mana", "Fragmento de Cristal"]
                itens_raros = ["Poção de Vida Grande", "Essência Mágica", "Pedra Elemental"]
                
                if inimigo.nivel <= 2:
                    item_drop = random.choice(itens_comuns)
                elif inimigo.nivel <= 5:
                    # 70% comum, 30% médio
                    item_drop = random.choice(itens_comuns) if random.random() < 0.7 else random.choice(itens_medios)
                else:
                    # 50% comum, 40% médio, 10% raro
                    roll = random.random()
                    if roll < 0.5:
                        item_drop = random.choice(itens_comuns)
                    elif roll < 0.9:
                        item_drop = random.choice(itens_medios)
                    else:
                        item_drop = random.choice(itens_raros)
            
            if item_drop:
                jogador.inventario.append(item_drop)
                mensagem += f"🎁 Item: *{item_drop}*\n"
            
            if subiu_nivel:
                mensagem += f"\n*PARABÉNS!* {msg_nivel} 🆙"
            
            # Adicionar mensagem de progresso do evento
            if esta_ativo_evento() and progresso and progresso["participando"] and 'mensagem_evento' in locals():
                mensagem += locals()['mensagem_evento']
            
            # Atualizar progresso de missão se aplicável
            if hasattr(jogador, 'missao_ativa') and jogador.missao_ativa:
                missao = jogador.missao_ativa
                if missao['tipo'] == 'batalha' and missao['inimigo_alvo'].lower() in inimigo.nome.lower():
                    missao['progresso'] += 1
                    
                    # Verificar se a missão foi concluída
                    if missao['progresso'] >= missao['quantidade_alvo']:
                        mensagem += f"\n\n🎯 *Missão Concluída!* A missão '{missao['titulo']}' foi completada.\nUse o comando /missao para receber sua recompensa."
                    else:
                        mensagem += f"\n\n🎯 Progresso de missão: {missao['progresso']}/{missao['quantidade_alvo']} {missao['inimigo_alvo']} derrotados."
            
            bot.reply_to(message, mensagem, parse_mode="Markdown")
            
            # Registrar atividade
            atividade_data = {
                "inimigo": inimigo.nome,
                "nivel_inimigo": inimigo.nivel,
                "moedas_ganhas": moedas_ganhas,
                "exp_ganha": exp_ganha,
                "item_drop": item_drop
            }
            
            # Adicionar informação de evento se aplicável
            if esta_ativo_evento() and progresso and progresso["participando"]:
                atividade_data["evento"] = {
                    "nome": evento_info['evento']['nome'],
                    "vitoria_registrada": True,
                    "vitorias_total": progresso_atualizado["vitorias"] if 'progresso_atualizado' in locals() else progresso["vitorias"]
                }
                
            db.registrar_atividade(message.from_user.id, "vitoria_batalha", atividade_data)
        
        # Salvar o jogador no banco de dados
        db.salvar_jogador(jogador)
    
    # Comando /loja
    @bot.message_handler(commands=["loja"])
    @rate_limit
    @monitor_requests('loja')
    def comando_loja(message):
        try:
            from .loja import mostrar_loja
            mostrar_loja(bot, message, jogadores, db, armas, armaduras, amuletos, consumiveis)
        except Exception as e:
            logger.error(f"Erro no comando loja: {str(e)}", exc_info=True)
            bot.reply_to(message, "⚠️ Ocorreu um erro ao acessar a loja. Por favor, tente novamente mais tarde.")
    
    # Handlers para navegação da loja
    @bot.message_handler(func=lambda msg: msg.text == "🗡️ Armas")
    def comando_mostrar_armas(message):
        try:
            from .loja import mostrar_armas
            mostrar_armas(bot, message, jogadores, db, armas)
        except Exception as e:
            logger.error(f"Erro ao mostrar armas: {str(e)}", exc_info=True)
            bot.reply_to(message, "⚠️ Ocorreu um erro ao mostrar as armas. Por favor, tente novamente mais tarde.")
    
    @bot.message_handler(func=lambda msg: msg.text == "🛡️ Armaduras")
    def comando_mostrar_armaduras(message):
        try:
            from .loja import mostrar_armaduras
            mostrar_armaduras(bot, message, jogadores, db, armaduras)
        except Exception as e:
            logger.error(f"Erro ao mostrar armaduras: {str(e)}", exc_info=True)
            bot.reply_to(message, "⚠️ Ocorreu um erro ao mostrar as armaduras. Por favor, tente novamente mais tarde.")
    
    @bot.message_handler(func=lambda msg: msg.text == "📿 Amuletos")
    def comando_mostrar_amuletos(message):
        try:
            from .loja import mostrar_amuletos
            mostrar_amuletos(bot, message, jogadores, db, amuletos)
        except Exception as e:
            logger.error(f"Erro ao mostrar amuletos: {str(e)}", exc_info=True)
            bot.reply_to(message, "⚠️ Ocorreu um erro ao mostrar os amuletos. Por favor, tente novamente mais tarde.")
    
    @bot.message_handler(func=lambda msg: msg.text == "🧪 Poções")
    def comando_mostrar_pocoes(message):
        try:
            from .loja import mostrar_pocoes
            mostrar_pocoes(bot, message, jogadores, db, consumiveis)
        except Exception as e:
            logger.error(f"Erro ao mostrar poções: {str(e)}", exc_info=True)
            bot.reply_to(message, "⚠️ Ocorreu um erro ao mostrar as poções. Por favor, tente novamente mais tarde.")
    
    @bot.message_handler(func=lambda msg: msg.text.startswith("Comprar "))
    def comando_comprar_item(message):
        try:
            from .loja import comprar_item
            comprar_item(bot, message, jogadores, db, armas, armaduras, amuletos, consumiveis)
        except Exception as e:
            logger.error(f"Erro ao comprar item: {str(e)}", exc_info=True)
            bot.reply_to(message, "⚠️ Ocorreu um erro ao processar sua compra. Por favor, tente novamente mais tarde.")
    
    @bot.message_handler(func=lambda msg: msg.text == "🔙 Voltar à Loja")
    def comando_voltar_loja(message):
        try:
            from .loja import mostrar_loja
            mostrar_loja(bot, message, jogadores, db, armas, armaduras, amuletos, consumiveis)
        except Exception as e:
            logger.error(f"Erro ao voltar para loja: {str(e)}", exc_info=True)
            bot.reply_to(message, "⚠️ Ocorreu um erro ao retornar à loja. Por favor, tente novamente mais tarde.")
    
    @bot.message_handler(func=lambda msg: msg.text == "📦 Ver Inventário")
    def comando_ver_inventario_pos_compra(message):
        try:
            from .inventario import mostrar_inventario
            mostrar_inventario(bot, message, jogadores)
        except Exception as e:
            logger.error(f"Erro ao mostrar inventário: {str(e)}", exc_info=True)
            bot.reply_to(message, "⚠️ Ocorreu um erro ao exibir seu inventário. Por favor, tente novamente mais tarde.")
    
    # Sistema de inventário
    @bot.message_handler(commands=["inventario"])
    @rate_limit
    @monitor_requests('inventario')
    def comando_inventario(message):
        try:
            from .inventario import mostrar_inventario
            mostrar_inventario(bot, message, jogadores)
        except Exception as e:
            logger.error(f"Erro no comando inventario: {str(e)}", exc_info=True)
            bot.reply_to(message, "⚠️ Ocorreu um erro ao acessar seu inventário. Por favor, tente novamente mais tarde.")
    
    @bot.message_handler(func=lambda msg: msg.text.startswith("Usar "))
    def comando_usar_item(message):
        try:
            from .inventario import usar_item
            usar_item(bot, message, jogadores, consumiveis)
        except Exception as e:
            logger.error(f"Erro ao usar item: {str(e)}", exc_info=True)
            bot.reply_to(message, "⚠️ Ocorreu um erro ao usar o item. Por favor, tente novamente mais tarde.")
    
    @bot.message_handler(func=lambda msg: msg.text == "Equipar" and hasattr(jogadores.get(msg.from_user.id, object()), "item_selecionado"))
    def comando_equipar_item(message):
        try:
            from .inventario import equipar_item
            equipar_item(bot, message, jogadores, armas, armaduras, amuletos)
        except Exception as e:
            logger.error(f"Erro ao equipar item: {str(e)}", exc_info=True)
            bot.reply_to(message, "⚠️ Ocorreu um erro ao equipar o item. Por favor, tente novamente mais tarde.")
    
    @bot.message_handler(func=lambda msg: msg.text == "Cancelar" and hasattr(jogadores.get(msg.from_user.id, object()), "item_selecionado"))
    def comando_cancelar_equipar(message):
        try:
            user_id = message.from_user.id
            jogador = jogadores[user_id]
            
            if hasattr(jogador, "item_selecionado"):
                delattr(jogador, "item_selecionado")
            
            bot.reply_to(message, "Operação cancelada.")
            from .inventario import mostrar_inventario
            mostrar_inventario(bot, message, jogadores)
        except Exception as e:
            logger.error(f"Erro ao cancelar equipar: {str(e)}", exc_info=True)
            bot.reply_to(message, "⚠️ Ocorreu um erro ao cancelar a operação. Por favor, tente novamente mais tarde.")
    
    # Sistema de missões
    @bot.message_handler(commands=["missao"])
    @rate_limit
    @monitor_requests('missao')
    def comando_missao(message):
        try:
            from .missoes import mostrar_missoes
            mostrar_missoes(bot, message, jogadores, db)
        except Exception as e:
            logger.error(f"Erro no comando missao: {str(e)}", exc_info=True)
            bot.reply_to(message, "⚠️ Ocorreu um erro ao acessar missões. Por favor, tente novamente mais tarde.")
    
    # Handlers para callback das missões
    @bot.callback_query_handler(func=lambda call: call.data == "aceitar_missao")
    def callback_aceitar_missao(call):
        try:
            from .missoes import processar_aceitacao_missao
            processar_aceitacao_missao(bot, call, jogadores, db)
        except Exception as e:
            logger.error(f"Erro ao aceitar missão: {str(e)}", exc_info=True)
            bot.answer_callback_query(call.id, "⚠️ Ocorreu um erro ao aceitar a missão. Por favor, tente novamente.")
    
    @bot.callback_query_handler(func=lambda call: call.data == "recusar_missao")
    def callback_recusar_missao(call):
        try:
            from .missoes import processar_recusa_missao
            processar_recusa_missao(bot, call, jogadores)
        except Exception as e:
            logger.error(f"Erro ao recusar missão: {str(e)}", exc_info=True)
            bot.answer_callback_query(call.id, "⚠️ Ocorreu um erro ao recusar a missão. Por favor, tente novamente.")
    
    @bot.callback_query_handler(func=lambda call: call.data == "receber_recompensa_missao")
    def callback_receber_recompensa_missao(call):
        try:
            from .missoes import processar_recompensa_missao
            processar_recompensa_missao(bot, call, jogadores, db)
        except Exception as e:
            logger.error(f"Erro ao receber recompensa: {str(e)}", exc_info=True)
            bot.answer_callback_query(call.id, "⚠️ Ocorreu um erro ao receber a recompensa. Por favor, tente novamente.")
            
    # Comando para voltar ao menu principal
    @bot.message_handler(func=lambda msg: msg.text == "🔙 Voltar")
    def voltar_menu_principal(message):
        try:
            # Voltar para o menu principal
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add("/perfil", "/batalha", "/missao")
            markup.add("/loja", "/inventario", "/evento")
            bot.reply_to(message, "Voltando ao menu principal. O que deseja fazer?", reply_markup=markup)
        except Exception as e:
            logger.error(f"Erro ao voltar ao menu principal: {str(e)}", exc_info=True)
            bot.reply_to(message, "⚠️ Ocorreu um erro ao voltar ao menu principal. Por favor, tente novamente mais tarde.")

    @bot.message_handler(func=lambda msg: msg.text == "💰 Vender Itens" or msg.text == "💰 Vender Mais Itens")
    def comando_mostrar_itens_venda(message):
        try:
            from .loja import mostrar_itens_venda
            mostrar_itens_venda(bot, message, jogadores, db, armas, armaduras, amuletos, consumiveis)
        except Exception as e:
            logger.error(f"Erro ao mostrar itens para venda: {str(e)}", exc_info=True)
            bot.reply_to(message, "⚠️ Ocorreu um erro ao mostrar seus itens para venda. Por favor, tente novamente mais tarde.")
    
    @bot.message_handler(func=lambda msg: msg.text.startswith("Vender "))
    def comando_vender_item(message):
        try:
            from .loja import vender_item
            vender_item(bot, message, jogadores, db, armas, armaduras, amuletos, consumiveis)
        except Exception as e:
            logger.error(f"Erro ao vender item: {str(e)}", exc_info=True)
            bot.reply_to(message, "⚠️ Ocorreu um erro ao processar sua venda. Por favor, tente novamente mais tarde.")

    logger.info("Comandos registrados com sucesso")
    return True 