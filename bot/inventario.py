# Arquivo para implementação do sistema de inventário
import logging
from telebot import types

logger = logging.getLogger(__name__)

def mostrar_inventario(bot, message, jogadores):
    """Mostra todos os itens no inventário do jogador"""
    try:
        user_id = message.from_user.id
        if user_id not in jogadores:
            bot.reply_to(message, "Você ainda não iniciou o jogo! Use /start primeiro.")
            return
        
        jogador = jogadores[user_id]
        
        if not jogador.inventario:
            bot.reply_to(message, "Seu inventário está vazio! 🎒\n\nVocê pode obter itens derrotando inimigos, completando missões ou comprando na loja.")
            return
        
        # Criar texto com a lista de itens no inventário agrupados por tipo
        from .itens import armas, armaduras, amuletos, consumiveis
        
        # Agrupar itens por categoria
        categorias = {
            "🗡️ Armas": [],
            "🛡️ Armaduras": [],
            "📿 Amuletos": [],
            "🧪 Poções": [],
            "📦 Outros": []
        }
        
        for item in jogador.inventario:
            if item in armas:
                categorias["🗡️ Armas"].append(item)
            elif item in armaduras:
                categorias["🛡️ Armaduras"].append(item)
            elif item in amuletos:
                categorias["📿 Amuletos"].append(item)
            elif item in consumiveis:
                categorias["🧪 Poções"].append(item)
            else:
                categorias["📦 Outros"].append(item)
        
        # Construir mensagem
        mensagem = "*Seu Inventário:*\n\n"
        
        for categoria, itens in categorias.items():
            if itens:
                mensagem += f"{categoria}:\n"
                for item in itens:
                    mensagem += f"- {item}\n"
                mensagem += "\n"
        
        # Botões para os itens no inventário
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2)
        botoes = []
        
        # Garantir que todos os itens no inventário tenham botões correspondentes
        for item in jogador.inventario:
            botoes.append(f"Usar {item}")
        
        # Organizar botões em pares (ou solitários se ímpar)
        for i in range(0, len(botoes), 2):
            if i + 1 < len(botoes):
                markup.add(botoes[i], botoes[i+1])
            else:
                markup.add(botoes[i])
        
        markup.add("🔙 Voltar")
        
        bot.reply_to(message, mensagem, parse_mode="Markdown", reply_markup=markup)
    except Exception as e:
        logger.error(f"Erro ao mostrar inventário: {str(e)}", exc_info=True)
        bot.reply_to(message, "⚠️ Ocorreu um erro ao exibir seu inventário. Por favor, tente novamente mais tarde.")

def usar_item(bot, message, jogadores, consumiveis):
    """Permite ao jogador usar um item do inventário"""
    try:
        user_id = message.from_user.id
        jogador = jogadores[user_id]
        
        # Extrair nome do item
        nome_item = message.text[4:].strip()  # Remove "Usar " do início e espaços extras
        
        # Verificar se o item está no inventário com verificação mais robusta
        item_encontrado = None
        for item in jogador.inventario:
            if item.lower() == nome_item.lower():
                item_encontrado = item
                break
        
        if not item_encontrado:
            # Log para debug do problema
            logger.debug(f"Item não encontrado no inventário. Usuário: {user_id}, Item: '{nome_item}'")
            logger.debug(f"Itens no inventário: {jogador.inventario}")
            
            bot.reply_to(message, f"Você não possui {nome_item} no seu inventário!")
            
            # Oferecer inventário atualizado
            mostrar_inventario(bot, message, jogadores)
            return
        
        # Usar o nome exato do item como está no inventário
        nome_item = item_encontrado
        
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
                # Verificar o tipo de buff
                if "duracao" in item_info:
                    # Adicionar buff temporário
                    novo_buff = {
                        "atributo": item_info["atributo"],
                        "valor": item_info["valor"],
                        "duracao": item_info["duracao"]
                    }
                    
                    if not hasattr(jogador, "buffs"):
                        jogador.buffs = []
                    
                    jogador.buffs.append(novo_buff)
                    
                    # Mensagem de feedback sobre o buff
                    if item_info["atributo"] == "forca":
                        bot.reply_to(message, f"Você usou *{nome_item}* e ganhou +{item_info['valor']} de força por {item_info['duracao']} turnos!\n\nForça atual: {jogador.forca} 💪", parse_mode="Markdown")
                    
                    elif item_info["atributo"] == "destreza":
                        bot.reply_to(message, f"Você usou *{nome_item}* e ganhou +{item_info['valor']} de destreza por {item_info['duracao']} turnos!\n\nDestreza atual: {jogador.destreza} 🏃", parse_mode="Markdown")
                    
                    elif item_info["atributo"] == "inteligencia":
                        bot.reply_to(message, f"Você usou *{nome_item}* e ganhou +{item_info['valor']} de inteligência por {item_info['duracao']} turnos!\n\nInteligência atual: {jogador.inteligencia} 🧠", parse_mode="Markdown")
                    
                    elif item_info["atributo"] == "todos":
                        # Aumentar todos os atributos
                        if not hasattr(jogador, "buffs"):
                            jogador.buffs = []
                        
                        # Adicionar buffs para cada atributo
                        for attr in ["forca", "destreza", "inteligencia"]:
                            jogador.buffs.append({
                                "atributo": attr,
                                "valor": item_info["valor"],
                                "duracao": item_info["duracao"]
                            })
                        
                        bot.reply_to(message, f"Você usou *{nome_item}* e ganhou +{item_info['valor']} em todos os atributos por {item_info['duracao']} turnos!\n\nForça: {jogador.forca} 💪\nDestreza: {jogador.destreza} 🏃\nInteligência: {jogador.inteligencia} 🧠", parse_mode="Markdown")
                
                else:
                    # Buff permanente
                    if item_info["atributo"] == "forca":
                        jogador.forca += item_info["valor"]
                        bot.reply_to(message, f"Você usou *{nome_item}* e ganhou +{item_info['valor']} de força permanentemente!\n\nForça atual: {jogador.forca} 💪", parse_mode="Markdown")
                    
                    elif item_info["atributo"] == "destreza":
                        jogador.destreza += item_info["valor"]
                        bot.reply_to(message, f"Você usou *{nome_item}* e ganhou +{item_info['valor']} de destreza permanentemente!\n\nDestreza atual: {jogador.destreza} 🏃", parse_mode="Markdown")
                    
                    elif item_info["atributo"] == "inteligencia":
                        jogador.inteligencia += item_info["valor"]
                        bot.reply_to(message, f"Você usou *{nome_item}* e ganhou +{item_info['valor']} de inteligência permanentemente!\n\nInteligência atual: {jogador.inteligencia} 🧠", parse_mode="Markdown")
                    
                    elif item_info["atributo"] == "todos":
                        jogador.forca += item_info["valor"]
                        jogador.destreza += item_info["valor"]
                        jogador.inteligencia += item_info["valor"]
                        bot.reply_to(message, f"Você usou *{nome_item}* e ganhou +{item_info['valor']} em todos os atributos permanentemente!\n\nForça: {jogador.forca} 💪\nDestreza: {jogador.destreza} 🏃\nInteligência: {jogador.inteligencia} 🧠", parse_mode="Markdown")
            
            # Remover item do inventário após uso
            jogador.inventario.remove(nome_item)
            
            # Registrar atividade
            from .database import Database
            db = Database()
            db.registrar_atividade(user_id, "usar_item", {
                "item": nome_item,
                "efeito": item_info["efeito"]
            })
        
        # Se for um equipamento, oferecer para equipar
        else:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add("Equipar", "Cancelar")
            
            # Armazenar temporariamente o item selecionado
            jogador.item_selecionado = nome_item
            
            bot.reply_to(message, f"Deseja equipar *{nome_item}*?", parse_mode="Markdown", reply_markup=markup)
        
        # Salvar jogador no banco de dados após usar o item
        from .database import Database
        db = Database()
        db.salvar_jogador(jogador)
    except Exception as e:
        logger.error(f"Erro ao usar item: {str(e)}", exc_info=True)
        bot.reply_to(message, "⚠️ Ocorreu um erro ao usar o item. Por favor, tente novamente mais tarde.")

def equipar_item(bot, message, jogadores, armas, armaduras, amuletos):
    """Permite ao jogador equipar um item de seu inventário"""
    try:
        user_id = message.from_user.id
        jogador = jogadores[user_id]
        
        # Verificar se há um item selecionado
        if not hasattr(jogador, "item_selecionado"):
            bot.reply_to(message, "Nenhum item selecionado para equipar.")
            return
        
        nome_item = jogador.item_selecionado
        
        # Verificar se o item está no inventário
        item_encontrado = None
        for item in jogador.inventario:
            if item.lower() == nome_item.lower():
                item_encontrado = item
                break
        
        if not item_encontrado:
            bot.reply_to(message, f"Você não possui {nome_item} no seu inventário!")
            delattr(jogador, "item_selecionado")
            return
        
        # Usar o nome exato do item como está no inventário
        nome_item = item_encontrado
        
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
        from .database import Database
        db = Database()
        db.salvar_jogador(jogador)
        
        # Registrar atividade
        db.registrar_atividade(user_id, "equipar_item", {
            "item": nome_item,
            "tipo": tipo_item
        })
    except Exception as e:
        logger.error(f"Erro ao equipar item: {str(e)}", exc_info=True)
        bot.reply_to(message, "⚠️ Ocorreu um erro ao equipar o item. Por favor, tente novamente mais tarde.") 