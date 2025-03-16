from typing import Optional
from telegram import Update
from telegram.ext import ContextTypes
import logging
from prometheus_client import Counter, Gauge

logger = logging.getLogger(__name__)

# Métricas Prometheus
ERROR_COUNTER = Counter('bot_errors', 'Contador de erros por tipo', ['error_type'])
ACTIVE_USERS_GAUGE = Gauge('active_users', 'Usuários ativos no momento')

class CustomError(Exception):
    """Exceção base para erros personalizados"""
    def __init__(self, message: str, user_friendly: Optional[str] = None):
        super().__init__(message)
        self.user_friendly = user_friendly or "Ocorreu um erro inesperado"
        ERROR_COUNTER.labels(error_type='custom').inc()

class DatabaseError(CustomError):
    """Erro de banco de dados"""
    def __init__(self, message: str):
        super().__init__(message, "Erro de conexão com o banco de dados")
        ERROR_COUNTER.labels(error_type='database').inc()

class APIConnectionError(CustomError):
    """Erro de conexão com API externa"""
    def __init__(self, message: str):
        super().__init__(message, "Erro de conexão com serviços externos")
        ERROR_COUNTER.labels(error_type='api').inc()

async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    error = getattr(context, 'error', None)
    
    if isinstance(error, CustomError):
        user_message = error.user_friendly
        log_level = logging.WARNING
    else:
        user_message = "Erro interno do sistema. Por favor, tente novamente mais tarde."
        log_level = logging.ERROR
    
    logger.log(log_level, msg="Exceção ocorrida:", exc_info=error)
    
    if update.effective_message:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"⚠️ {user_message}"
        )
    
    # Atualizar métricas
    ACTIVE_USERS_GAUGE.dec() 