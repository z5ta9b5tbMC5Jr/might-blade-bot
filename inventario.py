# Arquivo para implementação do sistema de inventário

def mostrar_inventario(bot, message, jogadores):
    user_id = message.from_user.id
    if user_id not in jogadores:
        bot.reply_to(message, "Você ainda não iniciou o jogo! Use /start primeiro.")
        return
    
    jogador = jogadores[user_id]
    
    if not jogador.inventario:
        bot.reply_to(message, "Seu inventário está vazio! 🎒\n\nVocê pode obter itens derrotando inimigos, completando missões ou comprando na loja.")
        return
    
    from telebot import types
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    
    # Adicionar botões para cada item no inventário
    for item in jogador.inventario:
        markup.add(f"Usar {item}")
    
    markup.add("Voltar")
    
    bot.reply_to(message, "*Seu Inventário:*\n\nSelecione um item para usar:", parse_mode="Markdown", reply_markup=markup)

def usar_item(bot, message, jogadores, consumiveis):
    user_id = message.from_user.id
    jogador = jogadores[user_id]
    
    # Extrair nome do item
    nome_item = message.text[4:]  # Remove "Usar " do início
    
    # Verificar se o item está no inventário
    if nome_item not in jogador.inventario:
        bot.reply_to(message, f"Você não possui {nome_item} no seu inventário!")
        return
    
    # Verificar se é um consumível
    if nome_item in consumiveis:
        item_info = consumiveis[nome_item]
        
        # Aplicar efeito do item
        if item_info["efeito"] == "vida":
            vida_anterior = jogador.vida
            jogador.vida = min(jogador.vida + item_info["valor"], jogador.vida_maxima)
            bot.reply_to(message, f"Você usou *{nome_item}* e recuperou {jogador.vida - vida_anterior} pontos de vida!\n\nVida atual: {jogador.vida}/{jogador.vida_maxima} ❤️", parse_mode="Markdown")
        
        elif item_info["efeito"] == "mana":
            mana_anterior = jogador.mana
            jogador.mana = min(jogador.mana + item_info["valor"], jogador.mana_maxima)
            bot.reply_to(message, f"Você usou *{nome_item}* e recuperou {jogador.mana - mana_anterior} pontos de mana!\n\nMana atual: {jogador.mana}/{jogador.mana_maxima} 🔮", parse_mode="Markdown")
        
        elif item_info["efeito"] == "buff":
            # Implementar sistema de buffs temporários
            if item_info["atributo"] == "forca":
                jogador.forca += item_info["valor"]
                # Aqui seria ideal implementar um sistema de duração para o buff
                bot.reply_to(message, f"Você usou *{nome_item}* e ganhou +{item_info['valor']} de força por {item_info['duracao']} turnos!\n\nForça atual: {jogador.forca} 💪", parse_mode="Markdown")
            
            elif item_info["atributo"] == "destreza":
                jogador.destreza += item_info["valor"]
                bot.reply_to(message, f"Você usou *{nome_item}* e ganhou +{item_info['valor']} de destreza por {item_info['duracao']} turnos!\n\nDestreza atual: {jogador.destreza} 🏃", parse_mode="Markdown")
            
            elif item_info["atributo"] == "inteligencia":
                jogador.inteligencia += item_info["valor"]
                bot.reply_to(message, f"Você usou *{nome_item}* e ganhou +{item_info['valor']} de inteligência por {item_info['duracao']} turnos!\n\nInteligência atual: {jogador.inteligencia} 🧠", parse_mode="Markdown")
            
            elif item_info["atributo"] == "todos":
                jogador.forca += item_info["valor"]
                jogador.destreza += item_info["valor"]
                jogador.inteligencia += item_info["valor"]
                bot.reply_to(message, f"Você usou *{nome_item}* e ganhou +{item_info['valor']} em todos os atributos por {item_info['duracao']} turnos!\n\nForça: {jogador.forca} 💪\nDestreza: {jogador.destreza} 🏃\nInteligência: {jogador.inteligencia} 🧠", parse_mode="Markdown")
        
        # Remover item do inventário após uso
        jogador.inventario.remove(nome_item)
    
    # Se for um equipamento, oferecer para equipar
    else:
        from telebot import types
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add("Equipar", "Cancelar")
        
        # Armazenar temporariamente o item selecionado
        jogador.item_selecionado = nome_item
        
        bot.reply_to(message, f"Deseja equipar *{nome_item}*?", parse_mode="Markdown", reply_markup=markup)
    
    # Salvar jogador no banco de dados após usar o item
    from bot import db
    db.salvar_jogador(jogador)

def equipar_item(bot, message, jogadores, armas, armaduras, amuletos):
    user_id = message.from_user.id
    jogador = jogadores[user_id]
    
    # Verificar se há um item selecionado
    if not hasattr(jogador, "item_selecionado"):
        bot.reply_to(message, "Nenhum item selecionado para equipar.")
        return
    
    nome_item = jogador.item_selecionado
    
    # Determinar o tipo de item
    tipo_item = None
    if nome_item in armas:
        tipo_item = "arma"
    elif nome_item in armaduras:
        tipo_item = "armadura"
    elif nome_item in amuletos:
        tipo_item = "amuleto"
    
    if not tipo_item:
        bot.reply_to(message, f"Não foi possível identificar o tipo do item {nome_item}.")
        delattr(jogador, "item_selecionado")
        return
    
    # Verificar restrições de classe
    if tipo_item in ["arma", "armadura"]:
        item_info = armas[nome_item] if tipo_item == "arma" else armaduras[nome_item]
        if "classe" in item_info and item_info["classe"] != jogador.classe and item_info["classe"] != "Qualquer":
            bot.reply_to(message, f"Você não pode equipar *{nome_item}* com a classe {jogador.classe}!", parse_mode="Markdown")
            delattr(jogador, "item_selecionado")
            return
    
    # Equipar o item
    if jogador.equipamento[tipo_item]:
        # Guardar item atual no inventário
        jogador.inventario.append(jogador.equipamento[tipo_item])
    
    # Remover o novo item do inventário e equipá-lo
    jogador.inventario.remove(nome_item)
    jogador.equipamento[tipo_item] = nome_item
    
    bot.reply_to(message, f"Você equipou *{nome_item}*!", parse_mode="Markdown")
    
    # Remover o item selecionado temporário
    delattr(jogador, "item_selecionado")
    
    # Salvar jogador no banco de dados após equipar o item
    from bot import db
    db.salvar_jogador(jogador)