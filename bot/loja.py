import logging
from telebot import types

logger = logging.getLogger(__name__)

def mostrar_loja(bot, message, jogadores, db, armas, armaduras, amuletos, consumiveis):
    """Mostra o menu principal da loja"""
    user_id = message.from_user.id
    if user_id not in jogadores:
        bot.reply_to(message, "Você ainda não iniciou o jogo! Use /start primeiro.")
        return
    
    jogador = jogadores[user_id]
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("🗡️ Armas", "🛡️ Armaduras")
    markup.add("📿 Amuletos", "🧪 Poções")
    markup.add("💰 Vender Itens", "🔙 Voltar")
    
    bot.reply_to(message, 
        f"*Bem-vindo à Loja do Might Blade!* 🏪\n\n"
        f"Você possui {jogador.moedas} moedas 💰\n\n"
        f"Selecione uma categoria para ver os itens disponíveis:",
        parse_mode="Markdown", 
        reply_markup=markup
    )

def mostrar_armas(bot, message, jogadores, db, armas):
    """Mostra as armas disponíveis para compra"""
    user_id = message.from_user.id
    jogador = jogadores[user_id]
    
    mensagem = "*Armas Disponíveis:*\n\n"
    itens_venda = []
    
    # Filtrar armas por classe do jogador
    for nome, detalhes in armas.items():
        if jogador.classe == detalhes["classe"] or detalhes["classe"] == "Qualquer":
            mensagem += f"🗡️ *{nome}*\n"
            mensagem += f"Dano: {detalhes['dano']}\n"
            mensagem += f"Preço: {detalhes['preco']} moedas\n"
            mensagem += f"Descrição: {detalhes['descricao']}\n\n"
            itens_venda.append(f"Comprar {nome}")
    
    # Se não houver itens para a classe do jogador
    if not itens_venda:
        mensagem += "Não há armas disponíveis para a sua classe no momento."
    
    itens_venda.append("🔙 Voltar à Loja")
    
    # Criar teclado de compra
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for item in itens_venda:
        markup.add(item)
    
    bot.reply_to(message, mensagem, parse_mode="Markdown", reply_markup=markup)

def mostrar_armaduras(bot, message, jogadores, db, armaduras):
    """Mostra as armaduras disponíveis para compra"""
    user_id = message.from_user.id
    jogador = jogadores[user_id]
    
    mensagem = "*Armaduras Disponíveis:*\n\n"
    itens_venda = []
    
    # Filtrar armaduras por classe do jogador
    for nome, detalhes in armaduras.items():
        if jogador.classe == detalhes["classe"] or detalhes["classe"] == "Qualquer":
            mensagem += f"🛡️ *{nome}*\n"
            mensagem += f"Defesa: {detalhes['defesa']}\n"
            mensagem += f"Preço: {detalhes['preco']} moedas\n"
            mensagem += f"Descrição: {detalhes['descricao']}\n\n"
            itens_venda.append(f"Comprar {nome}")
    
    # Se não houver itens para a classe do jogador
    if not itens_venda:
        mensagem += "Não há armaduras disponíveis para a sua classe no momento."
    
    itens_venda.append("🔙 Voltar à Loja")
    
    # Criar teclado de compra
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for item in itens_venda:
        markup.add(item)
    
    bot.reply_to(message, mensagem, parse_mode="Markdown", reply_markup=markup)

def mostrar_amuletos(bot, message, jogadores, db, amuletos):
    """Mostra os amuletos disponíveis para compra"""
    user_id = message.from_user.id
    jogador = jogadores[user_id]
    
    mensagem = "*Amuletos Disponíveis:*\n\n"
    itens_venda = []
    
    # Listar todos os amuletos
    for nome, detalhes in amuletos.items():
        mensagem += f"📿 *{nome}*\n"
        
        # Listar bônus do amuleto
        for atributo, valor in detalhes["bonus"].items():
            mensagem += f"{atributo.capitalize()}: +{valor}\n"
        
        mensagem += f"Preço: {detalhes['preco']} moedas\n"
        mensagem += f"Descrição: {detalhes['descricao']}\n\n"
        itens_venda.append(f"Comprar {nome}")
    
    # Se não houver itens disponíveis
    if not itens_venda:
        mensagem += "Não há amuletos disponíveis no momento."
    
    itens_venda.append("🔙 Voltar à Loja")
    
    # Criar teclado de compra
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for item in itens_venda:
        markup.add(item)
    
    bot.reply_to(message, mensagem, parse_mode="Markdown", reply_markup=markup)

def mostrar_pocoes(bot, message, jogadores, db, consumiveis):
    """Mostra as poções e consumíveis disponíveis para compra"""
    user_id = message.from_user.id
    jogador = jogadores[user_id]
    
    mensagem = "*Poções e Consumíveis Disponíveis:*\n\n"
    itens_venda = []
    
    # Listar todos os consumíveis
    for nome, detalhes in consumiveis.items():
        if detalhes.get("compravel", True):  # Verificar se o item pode ser comprado
            mensagem += f"🧪 *{nome}*\n"
            
            # Descrição do efeito
            if detalhes["efeito"] == "vida":
                mensagem += f"Recupera {detalhes['valor']} pontos de vida\n"
            elif detalhes["efeito"] == "mana":
                mensagem += f"Recupera {detalhes['valor']} pontos de mana\n"
            elif detalhes["efeito"] == "buff":
                mensagem += f"Aumenta {detalhes['atributo']} em {detalhes['valor']} por {detalhes['duracao']} turnos\n"
            
            mensagem += f"Preço: {detalhes['preco']} moedas\n"
            mensagem += f"Descrição: {detalhes['descricao']}\n\n"
            itens_venda.append(f"Comprar {nome}")
    
    # Se não houver itens disponíveis
    if not itens_venda:
        mensagem += "Não há poções disponíveis no momento."
    
    itens_venda.append("🔙 Voltar à Loja")
    
    # Criar teclado de compra
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for item in itens_venda:
        markup.add(item)
    
    bot.reply_to(message, mensagem, parse_mode="Markdown", reply_markup=markup)

def comprar_item(bot, message, jogadores, db, armas, armaduras, amuletos, consumiveis):
    """Processa a compra de um item"""
    user_id = message.from_user.id
    jogador = jogadores[user_id]
    
    # Extrair o nome do item da mensagem
    nome_item = message.text[8:]  # Remove "Comprar " do início
    
    # Verificar em qual categoria o item se encontra
    categoria = None
    item_info = None
    
    if nome_item in armas:
        categoria = "arma"
        item_info = armas[nome_item]
    elif nome_item in armaduras:
        categoria = "armadura"
        item_info = armaduras[nome_item]
    elif nome_item in amuletos:
        categoria = "amuleto"
        item_info = amuletos[nome_item]
    elif nome_item in consumiveis:
        categoria = "consumivel"
        item_info = consumiveis[nome_item]
    
    # Verificar se o item existe
    if not categoria or not item_info:
        bot.reply_to(message, f"Item '{nome_item}' não encontrado na loja.")
        return
    
    # Verificar se o jogador tem moedas suficientes
    if jogador.moedas < item_info["preco"]:
        bot.reply_to(message, f"Você não tem moedas suficientes para comprar este item!\n\nPreço: {item_info['preco']} moedas\nSeu saldo: {jogador.moedas} moedas")
        return
    
    # Verificar restrições de classe para armas e armaduras
    if categoria in ["arma", "armadura"] and "classe" in item_info:
        if item_info["classe"] != "Qualquer" and item_info["classe"] != jogador.classe:
            bot.reply_to(message, f"Este item é exclusivo para a classe {item_info['classe']}! Você não pode utilizá-lo como {jogador.classe}.")
            return
    
    # Deduzir o preço
    jogador.moedas -= item_info["preco"]
    
    # Processar de acordo com a categoria
    if categoria == "consumivel":
        jogador.inventario.append(nome_item)
        bot.reply_to(message, 
            f"Você comprou *{nome_item}* por {item_info['preco']} moedas! 💰\n\n"
            f"O item foi adicionado ao seu inventário. Use /inventario para utilizá-lo.", 
            parse_mode="Markdown"
        )
    elif categoria == "arma":
        # Adicionar ao equipamento ou substituir existente
        if jogador.equipamento["arma"]:
            jogador.inventario.append(jogador.equipamento["arma"])  # Guardar arma antiga no inventário
        jogador.equipamento["arma"] = nome_item
        bot.reply_to(message, 
            f"Você comprou e equipou *{nome_item}* por {item_info['preco']} moedas! 💰\n\n"
            f"Sua arma anterior foi movida para o inventário.", 
            parse_mode="Markdown"
        )
    elif categoria == "armadura":
        # Adicionar ao equipamento ou substituir existente
        if jogador.equipamento["armadura"]:
            jogador.inventario.append(jogador.equipamento["armadura"])  # Guardar armadura antiga no inventário
        jogador.equipamento["armadura"] = nome_item
        bot.reply_to(message, 
            f"Você comprou e equipou *{nome_item}* por {item_info['preco']} moedas! 💰\n\n"
            f"Sua armadura anterior foi movida para o inventário.", 
            parse_mode="Markdown"
        )
    elif categoria == "amuleto":
        # Adicionar ao equipamento ou substituir existente
        if jogador.equipamento["amuleto"]:
            jogador.inventario.append(jogador.equipamento["amuleto"])  # Guardar amuleto antigo no inventário
        jogador.equipamento["amuleto"] = nome_item
        bot.reply_to(message, 
            f"Você comprou e equipou *{nome_item}* por {item_info['preco']} moedas! 💰\n\n"
            f"Seu amuleto anterior foi movido para o inventário.", 
            parse_mode="Markdown"
        )
    
    # Registrar atividade
    db.registrar_atividade(user_id, "compra_item", {
        "item": nome_item,
        "categoria": categoria,
        "preco": item_info["preco"]
    })
    
    # Salvar jogador no banco de dados após a compra
    db.salvar_jogador(jogador)
    
    # Oferecer opção de voltar à loja
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("🔙 Voltar à Loja", "📦 Ver Inventário")
    
    bot.reply_to(message, "O que deseja fazer agora?", reply_markup=markup)

def mostrar_itens_venda(bot, message, jogadores, db, armas, armaduras, amuletos, consumiveis):
    """Mostra os itens do inventário do jogador disponíveis para venda"""
    user_id = message.from_user.id
    jogador = jogadores[user_id]
    
    # Verificar se o jogador tem itens no inventário
    if not jogador.inventario:
        bot.reply_to(message, 
            "📦 *Seu inventário está vazio*\n\n"
            "Você não possui itens para vender. Volte quando tiver algum equipamento para negociar.",
            parse_mode="Markdown",
            reply_markup=types.ReplyKeyboardMarkup(one_time_keyboard=True).add("🔙 Voltar à Loja")
        )
        return
    
    mensagem = "*Itens Disponíveis para Venda:*\n\n"
    itens_venda = []
    
    # Agrupar itens por categoria para melhor visualização
    armas_inventario = []
    armaduras_inventario = []
    amuletos_inventario = []
    pocoes_inventario = []
    outros_inventario = []
    
    for item in jogador.inventario:
        # Verificar em qual categoria o item se encontra
        categoria = None
        item_info = None
        preco_venda = 0
        
        if item in armas:
            categoria = "arma"
            item_info = armas[item]
            preco_venda = int(item_info["preco"] * 0.6)  # 60% do valor original
            armas_inventario.append((item, preco_venda))
        elif item in armaduras:
            categoria = "armadura"
            item_info = armaduras[item]
            preco_venda = int(item_info["preco"] * 0.6)
            armaduras_inventario.append((item, preco_venda))
        elif item in amuletos:
            categoria = "amuleto"
            item_info = amuletos[item]
            preco_venda = int(item_info["preco"] * 0.6)
            amuletos_inventario.append((item, preco_venda))
        elif item in consumiveis:
            categoria = "consumivel"
            item_info = consumiveis[item]
            preco_venda = int(item_info["preco"] * 0.6)
            pocoes_inventario.append((item, preco_venda))
        else:
            # Itens que não estão nas listas principais
            outros_inventario.append((item, 0))  # Valor zero para itens não catalogados
    
    # Adicionar armas à mensagem
    if armas_inventario:
        mensagem += "🗡️ *ARMAS*\n"
        for item, preco in armas_inventario:
            mensagem += f"• {item} - {preco} moedas\n"
            itens_venda.append(f"Vender {item}")
        mensagem += "\n"
    
    # Adicionar armaduras à mensagem
    if armaduras_inventario:
        mensagem += "🛡️ *ARMADURAS*\n"
        for item, preco in armaduras_inventario:
            mensagem += f"• {item} - {preco} moedas\n"
            itens_venda.append(f"Vender {item}")
        mensagem += "\n"
    
    # Adicionar amuletos à mensagem
    if amuletos_inventario:
        mensagem += "📿 *AMULETOS*\n"
        for item, preco in amuletos_inventario:
            mensagem += f"• {item} - {preco} moedas\n"
            itens_venda.append(f"Vender {item}")
        mensagem += "\n"
    
    # Adicionar poções à mensagem
    if pocoes_inventario:
        mensagem += "🧪 *POÇÕES*\n"
        for item, preco in pocoes_inventario:
            mensagem += f"• {item} - {preco} moedas\n"
            itens_venda.append(f"Vender {item}")
        mensagem += "\n"
    
    # Adicionar outros itens à mensagem
    if outros_inventario:
        mensagem += "📦 *OUTROS ITENS*\n"
        for item, preco in outros_inventario:
            if preco > 0:
                mensagem += f"• {item} - {preco} moedas\n"
                itens_venda.append(f"Vender {item}")
            else:
                mensagem += f"• {item} - Não é possível vender\n"
        mensagem += "\n"
    
    mensagem += "💰 *Selecione um item para vender.*\n"
    mensagem += "Você receberá 60% do valor original de cada item."
    
    # Adicionar botões de navegação
    itens_venda.append("🔙 Voltar à Loja")
    
    # Criar teclado para venda
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for item in itens_venda:
        markup.add(item)
    
    bot.reply_to(message, mensagem, parse_mode="Markdown", reply_markup=markup)

def vender_item(bot, message, jogadores, db, armas, armaduras, amuletos, consumiveis):
    """Processa a venda de um item do inventário"""
    user_id = message.from_user.id
    jogador = jogadores[user_id]
    
    # Extrair o nome do item da mensagem
    nome_item = message.text[7:]  # Remove "Vender " do início
    
    # Verificar se o item existe no inventário
    if nome_item not in jogador.inventario:
        bot.reply_to(message, 
            f"❌ *Erro na Venda:* O item '{nome_item}' não foi encontrado em seu inventário.",
            parse_mode="Markdown"
        )
        return
    
    # Verificar se o item está equipado
    if (jogador.equipamento["arma"] == nome_item or 
        jogador.equipamento["armadura"] == nome_item or 
        jogador.equipamento["amuleto"] == nome_item):
        bot.reply_to(message, 
            f"❌ *Erro na Venda:* Não é possível vender um item equipado.\n"
            f"Desequipe o item '{nome_item}' primeiro usando o comando /inventario.",
            parse_mode="Markdown"
        )
        return
    
    # Verificar em qual categoria o item se encontra
    categoria = None
    item_info = None
    
    if nome_item in armas:
        categoria = "arma"
        item_info = armas[nome_item]
    elif nome_item in armaduras:
        categoria = "armadura"
        item_info = armaduras[nome_item]
    elif nome_item in amuletos:
        categoria = "amuleto"
        item_info = amuletos[nome_item]
    elif nome_item in consumiveis:
        categoria = "consumivel"
        item_info = consumiveis[nome_item]
    
    # Verificar se o item pode ser vendido
    if not categoria or not item_info:
        bot.reply_to(message, 
            f"❌ *Erro na Venda:* O item '{nome_item}' não pode ser vendido.",
            parse_mode="Markdown"
        )
        return
    
    # Calcular o valor de venda (60% do preço original)
    preco_venda = int(item_info["preco"] * 0.6)
    
    # Processar a venda
    jogador.moedas += preco_venda
    jogador.inventario.remove(nome_item)
    
    # Enviar mensagem de confirmação
    bot.reply_to(message, 
        f"✅ *Venda realizada com sucesso!*\n\n"
        f"Você vendeu *{nome_item}* por *{preco_venda} moedas* 💰\n\n"
        f"Seu saldo atual: {jogador.moedas} moedas\n"
        f"Deseja vender mais algum item?",
        parse_mode="Markdown",
        reply_markup=types.ReplyKeyboardMarkup(one_time_keyboard=True)
            .add("💰 Vender Mais Itens", "🔙 Voltar à Loja")
    )
    
    # Registrar atividade
    db.registrar_atividade(user_id, "venda_item", {
        "item": nome_item,
        "categoria": categoria,
        "preco_venda": preco_venda
    })
    
    # Salvar jogador no banco de dados após a venda
    db.salvar_jogador(jogador) 