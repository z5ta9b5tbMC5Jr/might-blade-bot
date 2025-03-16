import telebot
from telebot import types
import sqlite3
import json
import os
import threading
import time
import logging
import prometheus_client
from prometheus_client import Counter, Gauge
import datetime

# Importar módulos do bot
from .database import Database
from .jogador import Jogador
from .comandos import registrar_comandos
from .errors import handle_error, CustomError, DatabaseError, APIConnectionError
from .monitoring import start_http_server, monitor_requests
from .utils import rate_limit, db_retry, carregar_env
from .itens import armas, armaduras, amuletos, consumiveis
from .eventos import iniciar_evento_diario, verificar_fim_evento

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Middleware para tratamento de mensagens
def middleware_handler(bot_instance, message):
    """Middleware para manipulação de mensagens"""
    try:
        # Simplesmente passar a mensagem adiante
        return message
    except Exception as e:
        # Apenas logar o erro, não enviar mensagem para o usuário para evitar loops
        logger.error(f"Erro no middleware: {str(e)}", exc_info=True)
        return None

def main():
    """Função principal para iniciar o bot"""
    try:
        logger.info("Iniciando bot...")
        
        # Carregar variáveis de ambiente
        env_vars = carregar_env()
        
        # Verificar se as variáveis necessárias existem
        if not env_vars.get("TELEGRAM_TOKEN"):
            logger.error("Token do Telegram não encontrado nas variáveis de ambiente")
            return
        
        # Inicializar banco de dados
        db = Database()
        logger.info("Banco de dados inicializado")
        
        # Inicializar bot do Telegram
        telebot.apihelper.ENABLE_MIDDLEWARE = True  # Habilitar middleware antes de inicializar o bot
        bot = telebot.TeleBot(env_vars["TELEGRAM_TOKEN"])
        
        # Dicionário de jogadores ativos
        jogadores = {}
        
        # Iniciar servidor Prometheus
        start_http_server(8000)
        logger.info("Servidor Prometheus iniciado na porta 8000")
        
        # Registrar handlers de comandos
        registrar_comandos(bot, jogadores, db, logger)
        
        # Registrar middleware para manipulação de mensagens
        bot.middleware_handler(middleware_handler)
        
        # Erro handler para capturar exceções
        @bot.middleware_handler(update_types=['message'])
        def error_handler_middleware(bot_instance, update):
            """Middleware para capturar erros em todos os handlers"""
            try:
                # Continuar normalmente com a próxima função na pilha
                return update
            except Exception as e:
                # Registrar erro sem enviar mensagem ao usuário (para evitar loops)
                logger.error(f"Erro capturado no middleware: {str(e)}", exc_info=True)
                return None
        
        # Comando /start
        @bot.message_handler(commands=["start"])
        def start_command(message):
            try:
                user_id = message.from_user.id
                username = message.from_user.username or message.from_user.first_name
                
                # Verificar se o jogador já existe no banco de dados
                jogador = db.carregar_jogador(user_id)
                if not jogador:
                    # Criar novo jogador
                    jogador = Jogador(user_id, username)
                    db.salvar_jogador(jogador)
                    
                    # Registrar atividade
                    db.registrar_atividade(user_id, "novo_jogador", {})
                    
                    bot.reply_to(message, 
                        f"Bem-vindo, {username}! 🎮\n\n"
                        "Você acaba de entrar no mundo de *Might Blade*! Use o comando /help para ver os comandos disponíveis.\n\n"
                        "Para começar sua aventura, escolha uma classe com o comando /classe!", 
                        parse_mode="Markdown"
                    )
                else:
                    # Jogador existente
                    bot.reply_to(message, 
                        f"Bem-vindo de volta, {username}! 🎮\n\n"
                        "Use o comando /help para ver os comandos disponíveis ou /perfil para ver seu status atual.",
                        parse_mode="Markdown"
                    )
                
                # Adicionar jogador à memória
                jogadores[user_id] = jogador
                
            except Exception as e:
                handle_error(e, bot, message, logger)
        
        # Inicializar eventos diários
        def eventos_scheduler():
            """Thread para gerenciar eventos diários"""
            logger.info("Iniciando agendador de eventos")
            
            # Verificar eventos diariamente (a cada hora)
            while True:
                try:
                    agora = datetime.datetime.now()
                    
                    # Iniciar evento às 00:00
                    if agora.hour == 0 and agora.minute < 5:
                        logger.info("Hora de iniciar novo evento diário")
                        iniciar_evento_diario(bot, jogadores, db, logger)
                    
                    # Verificar fim do evento a cada hora
                    verificar_fim_evento(bot, jogadores, db, logger)
                    
                except Exception as e:
                    logger.error(f"Erro no agendador de eventos: {e}", exc_info=True)
                
                # Aguardar 5 minutos antes de verificar novamente
                time.sleep(300)
        
        # Iniciar thread do agendador de eventos
        eventos_thread = threading.Thread(target=eventos_scheduler, daemon=True)
        eventos_thread.start()
        
        # Iniciar pooling
        logger.info("Bot iniciado com sucesso!")
        bot.infinity_polling()
        
    except Exception as e:
        logger.error(f"Erro ao iniciar o bot: {str(e)}", exc_info=True)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Bot encerrado pelo usuário")
    except Exception as e:
        logger.critical(f"Erro não tratado: {str(e)}", exc_info=True) 