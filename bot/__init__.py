# Pacote do bot Might Blade
# Este arquivo torna a pasta bot um pacote Python

from .bot import main, middleware_handler
from .jogador import Jogador
from .database import Database
from .errors import CustomError, DatabaseError, APIConnectionError, handle_error
from .utils import rate_limit, db_retry, carregar_env
from .monitoring import monitor_requests, REQUEST_TIME, COMMAND_COUNTER
from .eventos import (
    iniciar_evento_diario, 
    verificar_fim_evento, 
    obter_modificador_evento, 
    esta_ativo_evento, 
    obter_evento_atual,
    participar_evento,
    registrar_vitoria_evento,
    obter_progresso_jogador_evento,
    aplicar_modificador_evento
)
from .itens import armas, armaduras, amuletos, consumiveis, obter_item_por_nome, itens_por_classe, aplicar_efeito_item 