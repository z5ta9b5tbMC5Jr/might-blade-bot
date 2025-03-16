from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from .errors import CustomError, DatabaseError, APIConnectionError
import time
import os
import dotenv
import logging

logger = logging.getLogger(__name__)

# Remover dependência do pyrate_limiter
# Implementar nossa própria versão simplificada de rate limiting
user_last_request = {}  # Dicionário para rastrear o último tempo de requisição por usuário

def rate_limit(func):
    def wrapper(*args, **kwargs):
        # Como estamos tendo problemas com o middleware, vamos fazer um rate limit muito simples
        try:
            # Verificar se temos argumentos e se o primeiro é uma mensagem com from_user
            if args and hasattr(args[0], 'from_user') and hasattr(args[0].from_user, 'id'):
                user_id = args[0].from_user.id
                current_time = time.time()
                
                # Verificar se o usuário já fez uma requisição antes
                if user_id in user_last_request:
                    # Verificar se passou pelo menos 1 segundo desde a última requisição
                    if current_time - user_last_request[user_id] < 1:
                        # Não lançar erro, apenas ignorar requisições muito próximas
                        return
                
                # Atualizar o timestamp da última requisição
                user_last_request[user_id] = current_time
        except Exception as e:
            # Em caso de erro, apenas ignorar e continuar
            pass
            
        # Executar a função normalmente
        return func(*args, **kwargs)
    return wrapper

# Configuração de Retry Automático
db_retry = retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(1),
    retry=retry_if_exception_type((DatabaseError, APIConnectionError))
)

def carregar_env():
    """Carrega variáveis de ambiente do arquivo .env"""
    try:
        # Procurar pelo arquivo .env na pasta raiz do projeto
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
        
        # Verificar se o arquivo .env existe
        if os.path.exists(env_path):
            dotenv.load_dotenv(env_path)
            logger.info(f"Variáveis de ambiente carregadas de {env_path}")
        else:
            # Se não existir, tentar carregar do diretório atual
            env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
            if os.path.exists(env_path):
                dotenv.load_dotenv(env_path)
                logger.info(f"Variáveis de ambiente carregadas de {env_path}")
            else:
                logger.warning("Arquivo .env não encontrado. Usando variáveis de ambiente do sistema.")
        
        # Retornar um dicionário com as variáveis relevantes
        return {
            "TELEGRAM_TOKEN": os.getenv("TELEGRAM_TOKEN", "7789048923:AAEgePnqXLfWB6zqzSi0xAwkcJ87XUS24QQ"),
            "MONGODB_URI": os.getenv("MONGODB_URI", ""),
            "MONGODB_DB_NAME": os.getenv("MONGODB_DB_NAME", ""),
            "ENV": os.getenv("ENV", "development")
        }
    except Exception as e:
        logger.error(f"Erro ao carregar variáveis de ambiente: {e}", exc_info=True)
        # Retornar valores padrão em caso de erro
        return {
            "TELEGRAM_TOKEN": "7789048923:AAEgePnqXLfWB6zqzSi0xAwkcJ87XUS24QQ",
            "MONGODB_URI": "",
            "MONGODB_DB_NAME": "",
            "ENV": "development"
        } 