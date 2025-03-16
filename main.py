#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Might Blade Bot - Um bot de RPG para Telegram
Este é o ponto de entrada principal do bot.
"""

import logging
import sys
from bot import iniciar_bot

if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        handlers=[
            logging.FileHandler("bot.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Iniciando Might Blade Bot...")
        iniciar_bot()
    except KeyboardInterrupt:
        logger.info("Bot encerrado pelo usuário")
    except Exception as e:
        logger.critical(f"Erro fatal ao iniciar o bot: {str(e)}", exc_info=True)