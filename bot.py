import telebot
from telebot import types
import sqlite3
import json
import os
import schedule
import threading
import time
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes

# -*- coding: utf-8 -*-

# Classe Database (movida para o início)
class Database:
    def __init__(self, db_file="rpg_database.db"):
        self.db_file = db_file
        self.conn = None
        self.create_tables()
    
    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
            return self.conn
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return None
    
    def create_tables(self):
        try:
            conn = self.connect()
            if not conn:
                print("Não foi possível conectar ao banco de dados para criar tabelas")
                return
                
            cursor = conn.cursor()
            
            # Tabela de jogadores
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS jogadores (
                id INTEGER PRIMARY KEY,
                nome TEXT,
                classe TEXT,
                moedas INTEGER DEFAULT 100,
                nivel INTEGER DEFAULT 1,
                experiencia INTEGER DEFAULT 0,
                vida INTEGER DEFAULT 100,
                forca INTEGER DEFAULT 10,
                destreza INTEGER DEFAULT 10,
                inteligencia INTEGER DEFAULT 10,
                inventario TEXT,
                equipamento TEXT
            )
            ''')
            
            # Tabela de missões completadas
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS missoes_completadas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                jogador_id INTEGER,
                missao_id INTEGER,
                data_conclusao TEXT,
                FOREIGN KEY (jogador_id) REFERENCES jogadores (id)
            )
            ''')
            
            conn.commit()
        except sqlite3.Error as e:
            print(f"Erro ao criar tabelas: {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                conn.close()
    
    def salvar_jogador(self, jogador):
        try:
            conn = self.connect()
            if not conn:
                print("Não foi possível conectar ao banco de dados para salvar jogador")
                return False
                
            cursor = conn.cursor()
            
            # Converte inventário para JSON
            inventario_json = json.dumps(jogador.inventario)
            equipamento_json = json.dumps(jogador.equipamento)
            
            cursor.execute('''
            INSERT OR REPLACE INTO jogadores 
            (id, nome, classe, moedas, nivel, experiencia, vida, forca, destreza, inteligencia, inventario, equipamento)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                jogador.id, 
                jogador.nome, 
                jogador.classe, 
                jogador.moedas, 
                jogador.nivel, 
                jogador.experiencia, 
                jogador.vida,
                jogador.forca,
                jogador.destreza,
                jogador.inteligencia,
                inventario_json,
                equipamento_json
            ))
            
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao salvar jogador: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn:
                conn.close()
    
    def carregar_jogador(self, jogador_id):
        try:
            conn = self.connect()
            if not conn:
                print("Não foi possível conectar ao banco de dados para carregar jogador")
                return None
                
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM jogadores WHERE id = ?', (jogador_id,))
            dados = cursor.fetchone()
            
            if dados:
                try:
                    # Criar objeto jogador a partir dos dados
                    jogador = Jogador(
                        id=dados[0],
                        nome=dados[1],
                        classe=dados[2],
                        moedas=dados[3]
                    )
                    jogador.nivel = dados[4]
                    jogador.experiencia = dados[5]
                    jogador.vida = dados[6]
                    jogador.forca = dados[7]
                    jogador.destreza = dados[8]
                    jogador.inteligencia = dados[9]
                    jogador.inventario = json.loads(dados[10])
                    jogador.equipamento = json.loads(dados[11])
                    
                    return jogador
                except (json.JSONDecodeError, IndexError) as e:
                    print(f"Erro ao processar dados do jogador: {e}")
                    return None
            
            return None
        except sqlite3.Error as e:
            print(f"Erro ao carregar jogador: {e}")
            return None
        finally:
            if conn:
                conn.close()

# Inicializar o banco de dados
db = Database()

# Configuração do bot
API_KEY = "7789048923:AAEgePnqXLfWB6zqzSi0xAwkcJ87XUS24QQ"
bot = telebot.TeleBot(API_KEY)

# Estrutura de dados
class Jogador:
    def __init__(self, id, nome, classe, moedas=100):
        self.id = id
        self.nome = nome
        self.classe = classe
        self.moedas = moedas
        self.nivel = 1
        self.experiencia = 0
        self.vida = 100
        self.vida_maxima = 100
        self.mana = 50
        self.mana_maxima = 50
        self.inventario = []
        self.equipamento = {
            "arma": None,
            "armadura": None,
            "amuleto": None
        }
        
        # Atributos base
        self.forca = 10
        self.destreza = 10
        self.inteligencia = 10
        self.carisma = 10
        
        # Habilidades especiais
        self.habilidades = []
        
        # Definição de habilidades com base na classe
        if classe == "Guerreiro":
            self.forca += 5
            self.habilidades = ["Golpe Poderoso", "Escudo Protetor"]
        elif classe == "Mago":
            self.inteligencia += 5
            self.mana += 30
            self.mana_maxima += 30
            self.habilidades = ["Bola de Fogo", "Escudo Arcano"]
        elif classe == "Arqueiro":
            self.destreza += 5
            self.habilidades = ["Disparo Múltiplo", "Tiro Certeiro"]
    
    def subir_nivel(self):
        self.nivel += 1
        self.experiencia = 0
        
        # Aumenta atributos com base na classe
        if self.classe == "Guerreiro":
            self.forca += 2
            self.vida_maxima += 15
        elif self.classe == "Mago":
            self.inteligencia += 2
            self.mana_maxima += 10
        elif self.classe == "Arqueiro":
            self.destreza += 2
            self.vida_maxima += 10
        
        # Restaura vida e mana ao subir de nível
        self.vida = self.vida_maxima
        self.mana = self.mana_maxima
        
        # Adicionar novas habilidades com base no nível
        if self.nivel == 3:
            if self.classe == "Guerreiro":
                self.habilidades.append("Grito de Guerra")
            elif self.classe == "Mago":
                self.habilidades.append("Raio Elétrico")
            elif self.classe == "Arqueiro":
                self.habilidades.append("Chuva de Flechas")
    
    def usar_habilidade(self, habilidade_nome):
        if habilidade_nome not in self.habilidades:
            return False, "Você não possui essa habilidade!"
        
        # Dicionário com informações das habilidades: custo de mana e mensagem
        habilidades_info = {
            "Golpe Poderoso": {"mana": 10, "mensagem": f"*{self.nome}* usou *Golpe Poderoso*! 💪"},
            "Escudo Protetor": {"mana": 5, "mensagem": f"*{self.nome}* usou *Escudo Protetor*! 🛡️"},
            "Bola de Fogo": {"mana": 15, "mensagem": f"*{self.nome}* lançou *Bola de Fogo*! 🔥"},
            "Escudo Arcano": {"mana": 10, "mensagem": f"*{self.nome}* usou *Escudo Arcano*! 🧙"},
            "Grito de Guerra": {"mana": 12, "mensagem": f"*{self.nome}* usou *Grito de Guerra*! 🔊"},
            "Raio Elétrico": {"mana": 18, "mensagem": f"*{self.nome}* lançou *Raio Elétrico*! ⚡"},
            "Chuva de Flechas": {"mana": 15, "mensagem": f"*{self.nome}* usou *Chuva de Flechas*! 🏹"},
            "Disparo Múltiplo": {"mana": 12, "mensagem": f"*{self.nome}* usou *Disparo Múltiplo*! 🏹"},
            "Tiro Certeiro": {"mana": 8, "mensagem": f"*{self.nome}* usou *Tiro Certeiro*! 🎯"}
        }
        
        # Verificar se a habilidade está no dicionário
        if habilidade_nome in habilidades_info:
            info = habilidades_info[habilidade_nome]
            if self.mana < info["mana"]:
                return False, "Mana insuficiente!"
            self.mana -= info["mana"]
            return True, info["mensagem"]
        else:
            return False, "Habilidade desconhecida!"

# Dicionário para armazenar os jogadores
jogadores = {}

# Dicionários de itens
armas = {
    # Armas para Guerreiro
    "Espada Básica": {"dano": 5, "preco": 50, "classe": "Guerreiro", "descricao": "Uma espada simples mas eficiente."},
    "Espada Longa": {"dano": 8, "preco": 100, "classe": "Guerreiro", "descricao": "Uma espada de alcance maior e mais poder."},
    "Machado de Batalha": {"dano": 10, "preco": 150, "classe": "Guerreiro", "descricao": "Um machado pesado que causa dano devastador."},
    "Martelo de Guerra": {"dano": 12, "preco": 200, "classe": "Guerreiro", "descricao": "Um martelo poderoso que pode esmagar armaduras."},
    "Espada Flamejante": {"dano": 15, "preco": 300, "classe": "Guerreiro", "descricao": "Uma espada encantada com o poder do fogo."},
    
    # Armas para Arqueiro
    "Adaga Afiada": {"dano": 3, "preco": 30, "classe": "Arqueiro", "descricao": "Uma adaga leve e precisa."},
    "Arco Curto": {"dano": 5, "preco": 60, "classe": "Arqueiro", "descricao": "Um arco simples mas eficaz para iniciantes."},
    "Arco Élfico": {"dano": 7, "preco": 120, "classe": "Arqueiro", "descricao": "Um arco élfico refinado e preciso."},
    "Besta de Repetição": {"dano": 9, "preco": 180, "classe": "Arqueiro", "descricao": "Uma besta que permite disparos rápidos e precisos."},
    "Arco Longo de Precisão": {"dano": 12, "preco": 250, "classe": "Arqueiro", "descricao": "Um arco longo que permite atingir alvos distantes com precisão mortal."},
    
    # Armas para Mago
    "Cajado Iniciante": {"dano": 4, "preco": 40, "classe": "Mago", "descricao": "Um cajado para canalizar magia básica."},
    "Varinha Arcana": {"dano": 6, "preco": 80, "classe": "Mago", "descricao": "Uma varinha que amplifica feitiços básicos."},
    "Cajado Elemental": {"dano": 9, "preco": 130, "classe": "Mago", "descricao": "Um cajado que potencializa magias elementais."},
    "Orbe Místico": {"dano": 11, "preco": 200, "classe": "Mago", "descricao": "Um orbe que concentra energia mágica para feitiços poderosos."},
    "Cajado do Arquimago": {"dano": 14, "preco": 280, "classe": "Mago", "descricao": "Um cajado lendário que amplifica drasticamente o poder mágico."}
}

armaduras = {
    # Armaduras para Arqueiro
    "Armadura de Couro": {"defesa": 3, "preco": 40, "classe": "Arqueiro", "descricao": "Armadura leve feita de couro resistente."},
    "Capa do Caçador": {"defesa": 4, "preco": 70, "classe": "Arqueiro", "descricao": "Uma capa que oferece camuflagem e proteção leve."},
    "Armadura de Escamas": {"defesa": 6, "preco": 120, "classe": "Arqueiro", "descricao": "Armadura feita de escamas leves mas resistentes."},
    "Traje Élfico": {"defesa": 8, "preco": 180, "classe": "Arqueiro", "descricao": "Um traje élfico que combina leveza e proteção superior."},
    
    # Armaduras para Guerreiro
    "Armadura de Ferro": {"defesa": 5, "preco": 80, "classe": "Guerreiro", "descricao": "Armadura robusta que oferece boa proteção."},
    "Armadura de Placas": {"defesa": 8, "preco": 150, "classe": "Guerreiro", "descricao": "Armadura pesada que oferece excelente proteção."},
    "Armadura de Cavaleiro": {"defesa": 10, "preco": 220, "classe": "Guerreiro", "descricao": "Armadura completa digna de um cavaleiro real."},
    "Armadura Encantada": {"defesa": 12, "preco": 300, "classe": "Guerreiro", "descricao": "Armadura reforçada com encantamentos de proteção."},
    
    # Armaduras para Mago
    "Vestes Arcanas": {"defesa": 2, "mana": 10, "preco": 60, "classe": "Mago", "descricao": "Vestes que aumentam seu poder mágico."},
    "Manto do Sábio": {"defesa": 3, "mana": 15, "preco": 100, "classe": "Mago", "descricao": "Um manto que amplifica a regeneração de mana."},
    "Vestes Elementais": {"defesa": 4, "mana": 20, "preco": 160, "classe": "Mago", "descricao": "Vestes imbuídas com poder elemental que aumentam a potência de magias."},
    "Manto do Arquimago": {"defesa": 5, "mana": 30, "preco": 250, "classe": "Mago", "descricao": "Um manto lendário que oferece grande proteção mágica e reserva de mana."}
}

amuletos = {
    # Amuletos para todas as classes
    "Amuleto de Proteção": {"efeito": "defesa", "valor": 2, "preco": 50, "classe": "Qualquer", "descricao": "Um amuleto que oferece proteção adicional contra ataques."},
    "Amuleto da Sorte": {"efeito": "sorte", "valor": 5, "preco": 75, "classe": "Qualquer", "descricao": "Aumenta suas chances de encontrar itens raros."},
    "Amuleto de Vitalidade": {"efeito": "vida", "valor": 15, "preco": 90, "classe": "Qualquer", "descricao": "Aumenta a vida máxima do personagem."},
    
    # Amuletos para Guerreiro
    "Amuleto do Guerreiro": {"efeito": "forca", "valor": 3, "preco": 100, "classe": "Guerreiro", "descricao": "Aumenta a força do guerreiro em combate."},
    "Amuleto do Berserker": {"efeito": "furia", "valor": 5, "preco": 150, "classe": "Guerreiro", "descricao": "Aumenta o dano causado quando a vida está baixa."},
    "Amuleto do Campeão": {"efeito": "resistencia", "valor": 4, "preco": 200, "classe": "Guerreiro", "descricao": "Reduz o dano recebido em combate."},
    
    # Amuletos para Mago
    "Amuleto Arcano": {"efeito": "mana", "valor": 20, "preco": 100, "classe": "Mago", "descricao": "Aumenta a mana máxima do mago."},
    "Amuleto Elemental": {"efeito": "dano_magico", "valor": 4, "preco": 150, "classe": "Mago", "descricao": "Aumenta o dano de magias elementais."},
    "Amuleto do Arquimago": {"efeito": "regeneracao_mana", "valor": 3, "preco": 200, "classe": "Mago", "descricao": "Regenera mana durante o combate."},
    
    # Amuletos para Arqueiro
    "Amuleto do Caçador": {"efeito": "precisao", "valor": 3, "preco": 100, "classe": "Arqueiro", "descricao": "Aumenta a precisão dos ataques à distância."},
    "Amuleto da Águia": {"efeito": "critico", "valor": 5, "preco": 150, "classe": "Arqueiro", "descricao": "Aumenta a chance de acertos críticos."},
    "Amuleto do Vento": {"efeito": "velocidade", "valor": 4, "preco": 200, "classe": "Arqueiro", "descricao": "Aumenta a velocidade de ataque e movimento."}
}

consumiveis = {
    # Poções de Cura
    "Poção de Cura Pequena": {"efeito": "vida", "valor": 20, "preco": 15, "descricao": "Restaura 20 pontos de vida."},
    "Poção de Cura": {"efeito": "vida", "valor": 40, "preco": 30, "descricao": "Restaura 40 pontos de vida."},
    "Poção de Cura Grande": {"efeito": "vida", "valor": 70, "preco": 50, "descricao": "Restaura 70 pontos de vida."},
    "Elixir de Vida": {"efeito": "vida", "valor": 100, "preco": 80, "descricao": "Restaura toda a vida do personagem."},
    
    # Poções de Mana
    "Poção de Mana Pequena": {"efeito": "mana", "valor": 15, "preco": 20, "descricao": "Restaura 15 pontos de mana."},
    "Poção de Mana": {"efeito": "mana", "valor": 30, "preco": 35, "descricao": "Restaura 30 pontos de mana."},
    "Poção de Mana Grande": {"efeito": "mana", "valor": 50, "preco": 55, "descricao": "Restaura 50 pontos de mana."},
    "Elixir Arcano": {"efeito": "mana", "valor": 100, "preco": 90, "descricao": "Restaura toda a mana do personagem."},
    
    # Poções de Buff
    "Poção de Força": {"efeito": "buff", "atributo": "forca", "valor": 3, "duracao": 3, "preco": 35, "descricao": "Aumenta força em 3 por 3 turnos."},
    "Poção de Destreza": {"efeito": "buff", "atributo": "destreza", "valor": 3, "duracao": 3, "preco": 35, "descricao": "Aumenta destreza em 3 por 3 turnos."},
    "Poção de Inteligência": {"efeito": "buff", "atributo": "inteligencia", "valor": 3, "duracao": 3, "preco": 35, "descricao": "Aumenta inteligência em 3 por 3 turnos."},
    "Elixir do Herói": {"efeito": "buff", "atributo": "todos", "valor": 2, "duracao": 5, "preco": 75, "descricao": "Aumenta todos os atributos em 2 por 5 turnos."}
}

# Eventos globais do mundo
eventos_globais = {
    "Chuva de Meteoros": {
        "descricao": "Uma chuva de meteoros está ocorrendo! Os jogadores ganham +10% de experiência em batalhas.",
        "buff": {"tipo": "exp", "valor": 0.1},
        "duracao": 1  # em horas
    },
    "Eclipse Lunar": {
        "descricao": "Um eclipse lunar mágico está acontecendo! Os magos recebem +20% de dano mágico.",
        "buff": {"tipo": "dano", "classe": "Mago", "valor": 0.2},
        "duracao": 2  # em horas
    },
    "Festival do Guerreiro": {
        "descricao": "O festival anual dos guerreiros está ocorrendo! Guerreiros recebem desconto de 20% nas lojas.",
        "buff": {"tipo": "comercio", "classe": "Guerreiro", "valor": 0.2},
        "duracao": 3  # em horas
    }
}

evento_atual = None
hora_fim_evento = None

def iniciar_evento_aleatorio():
    global evento_atual, hora_fim_evento
    
    import random
    from datetime import datetime, timedelta
    
    # Escolher evento aleatório
    evento_escolhido = random.choice(list(eventos_globais.keys()))
    evento_atual = eventos_globais[evento_escolhido]
    
    # Definir hora de término
    hora_fim_evento = datetime.now() + timedelta(hours=evento_atual["duracao"])
    
    # Notificar todos os jogadores
    for user_id in jogadores:
        bot.send_message(user_id, f"*Evento Global: {evento_escolhido}*\n\n{evento_atual['descricao']}\n\nO evento durará por {evento_atual['duracao']} horas!", parse_mode="Markdown")

def verificar_fim_evento():
    global evento_atual, hora_fim_evento
    
    from datetime import datetime
    
    if evento_atual and datetime.now() >= hora_fim_evento:
        # Notificar fim do evento
        for user_id in jogadores:
            bot.send_message(user_id, "O evento global terminou! O mundo volta ao normal.")
        
        evento_atual = None
        hora_fim_evento = None

# Agendar eventos aleatórios a cada 6 horas
schedule.every(6).hours.do(iniciar_evento_aleatorio)

# Verificar fim de eventos a cada 10 minutos
schedule.every(10).minutes.do(verificar_fim_evento)

# Thread para executar agendamentos
def executar_agendamentos():
    while True:
        schedule.run_pending()
        time.sleep(60)

# Iniciar thread de agendamentos
threading.Thread(target=executar_agendamentos, daemon=True).start()

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Manipulador global de erros"""
    logger.error(msg="Exceção ocorrida:", exc_info=context.error)
    
    if update.effective_message:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="⚠️ Ops! Ocorreu um erro inesperado. Nossa equipe já foi notificada."
        )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # Sua lógica principal aqui
        await update.message.reply_text('Olá! Como posso ajudar?')
    except Exception as e:
        logger.error(f"Erro no comando /start: {str(e)}")
        await error_handler(update, context)

# Comandos básicos
@bot.message_handler(commands=["start"])
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await start(update, context)

@bot.message_handler(commands=["help"])
def help_command(message):
    bot.reply_to(message, "Comandos disponíveis:\n\n/start - Inicia o jogo\n/classe - Escolha sua classe\n/moedas - Veja suas moedas\n/perfil - Veja seu perfil\n/batalha - Inicie uma batalha\n/missao - Receba uma missão\n/loja - Acesse a loja\n/inventario - Veja e use itens do seu inventário")

@bot.message_handler(commands=["classe"])
def escolher_classe(message):
    user_id = message.from_user.id
    if user_id not in jogadores:
        bot.reply_to(message, "Você ainda não iniciou o jogo! Use /start primeiro.")
        return
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("Guerreiro", "Mago", "Arqueiro")
    bot.reply_to(message, "Escolha sua classe:", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text in ["Guerreiro", "Mago", "Arqueiro"])
def receber_classe(message):
    user_id = message.from_user.id
    if user_id not in jogadores:
        bot.reply_to(message, "Você ainda não iniciou o jogo! Use /start primeiro.")
        return
    
    jogadores[user_id].classe = message.text
    
    # Descrições das classes
    descricoes = {
        "Guerreiro": "💪 *Guerreiro*: Forte e resistente, especialista em combate corpo a corpo.",
        "Mago": "🧙 *Mago*: Domina as artes arcanas, capaz de lançar poderosos feitiços.",
        "Arqueiro": "🏹 *Arqueiro*: Ágil e preciso, especialista em ataques à distância."
    }
    
    bot.reply_to(message, f"Classe escolhida: {descricoes[message.text]}\n\nSua jornada começa agora! 🎉", parse_mode="Markdown")
    
    # Salvar jogador no banco de dados
    db.salvar_jogador(jogadores[user_id])

@bot.message_handler(commands=["moedas"])
def ver_moedas(message):
    user_id = message.from_user.id
    if user_id not in jogadores:
        bot.reply_to(message, "Você ainda não iniciou o jogo! Use /start primeiro.")
        return
    
    bot.reply_to(message, f"Você possui {jogadores[user_id].moedas} moedas 💰")

@bot.message_handler(commands=["perfil"])
def ver_perfil(message):
    user_id = message.from_user.id
    if user_id not in jogadores:
        bot.reply_to(message, "Você ainda não iniciou o jogo! Use /start primeiro.")
        return
    
    jogador = jogadores[user_id]
    classe = jogador.classe if jogador.classe else "Não definida"
    
    perfil = f"*Perfil de {jogador.nome}*\n\n"
    perfil += f"🎭 *Classe*: {classe}\n"
    perfil += f"💰 *Moedas*: {jogador.moedas}\n"
    perfil += f"⚔️ *Nível*: {jogador.nivel}\n"
    perfil += f"✨ *Experiência*: {jogador.experiencia}\n"
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
        perfil += "\n🎒 *Inventário*:\n"
        for item in jogador.inventario:
            perfil += f"- {item}\n"
    else:
        perfil += "\n🎒 *Inventário*: Vazio"
    
    # Habilidades
    if jogador.habilidades:
        perfil += "\n✨ *Habilidades*:\n"
        for habilidade in jogador.habilidades:
            perfil += f"- {habilidade}\n"
    
    bot.reply_to(message, perfil, parse_mode="Markdown")

# Sistema de batalha
@bot.message_handler(commands=["batalha"])
def iniciar_batalha(message):
    user_id = message.from_user.id
    if user_id not in jogadores:
        bot.reply_to(message, "Você ainda não iniciou o jogo! Use /start primeiro.")
        return
    
    jogador = jogadores[user_id]
    if not jogador.classe:
        bot.reply_to(message, "Você precisa escolher uma classe antes de batalhar! Use /classe.")
        return
    
    # Lista de inimigos
    inimigos = ["Goblin", "Lobo", "Bandido", "Esqueleto", "Slime"]
    import random
    inimigo = random.choice(inimigos)
    vida_inimigo = random.randint(50, 100)
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("Atacar", "Fugir")
    
    bot.reply_to(message, f"Você encontrou um *{inimigo}* com {vida_inimigo} de vida! ⚔️\n\nO que deseja fazer?", parse_mode="Markdown", reply_markup=markup)
    
    # Armazenar informações da batalha
    jogador.batalha = {"inimigo": inimigo, "vida_inimigo": vida_inimigo}

@bot.message_handler(func=lambda msg: msg.text == "Atacar" and hasattr(jogadores.get(msg.from_user.id, object()), "batalha"))
def atacar(message):
    user_id = message.from_user.id
    jogador = jogadores[user_id]
    
    # Calcular dano baseado na classe
    import random
    if jogador.classe == "Guerreiro":
        dano = random.randint(15, 25)
    elif jogador.classe == "Mago":
        dano = random.randint(10, 30)
    elif jogador.classe == "Arqueiro":
        dano = random.randint(12, 28)
    else:
        dano = random.randint(10, 20)
    
    # Atualizar vida do inimigo
    jogador.batalha["vida_inimigo"] -= dano
    
    if jogador.batalha["vida_inimigo"] <= 0:
        # Inimigo derrotado
        recompensa = random.randint(10, 30)
        experiencia = random.randint(5, 15)
        
        jogador.moedas += recompensa
        jogador.experiencia += experiencia
        
        # Verificar se subiu de nível
        if jogador.experiencia >= jogador.nivel * 20:
            jogador.nivel += 1
            jogador.experiencia = 0
            mensagem = f"Você derrotou o *{jogador.batalha['inimigo']}*! 🎉\n\nRecompensa: {recompensa} moedas 💰\nExperiência: {experiencia} pontos ✨\n\n*PARABÉNS! Você subiu para o nível {jogador.nivel}!* 🆙"
        else:
            mensagem = f"Você derrotou o *{jogador.batalha['inimigo']}*! 🎉\n\nRecompensa: {recompensa} moedas 💰\nExperiência: {experiencia} pontos ✨"
        
        # Chance de encontrar um item
        if random.random() < 0.3:  # 30% de chance
            itens = ["Poção de Cura", "Espada Enferrujada", "Escudo de Madeira", "Arco Velho", "Grimório Básico"]
            item = random.choice(itens)
            jogador.inventario.append(item)
            mensagem += f"\n\nVocê encontrou um item: *{item}*! 🎁"
        
        bot.reply_to(message, mensagem, parse_mode="Markdown")
        delattr(jogador, "batalha")
        
        # Salvar jogador no banco de dados
        db.salvar_jogador(jogador)
    else:
        # Inimigo ainda vivo, ele contra-ataca
        dano_inimigo = random.randint(5, 15)
        jogador.vida -= dano_inimigo
        
        if jogador.vida <= 0:
            # Jogador derrotado
            jogador.vida = 100
            perda = random.randint(5, 15)
            jogador.moedas = max(0, jogador.moedas - perda)
            
            bot.reply_to(message, f"Você foi derrotado pelo *{jogador.batalha['inimigo']}*! 😵\n\nVocê perdeu {perda} moedas.\nSua vida foi restaurada para 100.", parse_mode="Markdown")
            delattr(jogador, "batalha")
            
            # Salvar jogador no banco de dados
            db.salvar_jogador(jogador)
        else:
            # Batalha continua
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add("Atacar", "Fugir")
            
            bot.reply_to(message, f"Você causou *{dano}* de dano ao *{jogador.batalha['inimigo']}*!\nO inimigo contra-atacou e causou *{dano_inimigo}* de dano a você!\n\nSua vida: {jogador.vida}/100 ❤️\nVida do inimigo: {jogador.batalha['vida_inimigo']} ❤️\n\nO que deseja fazer?", parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text == "Fugir" and hasattr(jogadores.get(msg.from_user.id, object()), "batalha"))
def fugir(message):
    user_id = message.from_user.id
    jogador = jogadores[user_id]
    
    import random
    if random.random() < 0.7:  # 70% de chance de fugir
        bot.reply_to(message, f"Você fugiu com sucesso da batalha contra o *{jogador.batalha['inimigo']}*! 🏃‍♂️", parse_mode="Markdown")
        delattr(jogador, "batalha")
    else:
        # Falha ao fugir, inimigo ataca
        dano_inimigo = random.randint(5, 15)
        jogador.vida -= dano_inimigo
        
        if jogador.vida <= 0:
            # Jogador derrotado
            jogador.vida = 100
            perda = random.randint(5, 15)
            jogador.moedas = max(0, jogador.moedas - perda)
            
            bot.reply_to(message, f"Você falhou ao fugir e foi derrotado pelo *{jogador.batalha['inimigo']}*! 😵\n\nVocê perdeu {perda} moedas.\nSua vida foi restaurada para 100.", parse_mode="Markdown")
            delattr(jogador, "batalha")
            
            # Salvar jogador no banco de dados
            db.salvar_jogador(jogador)
        else:
            # Batalha continua
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add("Atacar", "Fugir")
            
            bot.reply_to(message, f"Você falhou ao fugir!\nO *{jogador.batalha['inimigo']}* atacou e causou *{dano_inimigo}* de dano a você!\n\nSua vida: {jogador.vida}/100 ❤️\nVida do inimigo: {jogador.batalha['vida_inimigo']} ❤️\n\nO que deseja fazer?", parse_mode="Markdown", reply_markup=markup)

# Sistema de missões
@bot.message_handler(commands=["missao"])
def obter_missao(message):
    user_id = message.from_user.id
    if user_id not in jogadores:
        bot.reply_to(message, "Você ainda não iniciou o jogo! Use /start primeiro.")
        return
    
    jogador = jogadores[user_id]
    if not jogador.classe:
        bot.reply_to(message, "Você precisa escolher uma classe antes de receber missões! Use /classe.")
        return
    
    # Lista de missões
    missoes = [
        {"titulo": "Caça aos Goblins", "descricao": "Derrote 3 goblins que estão aterrorizando a vila.", "recompensa": 50},
        {"titulo": "Ervas Medicinais", "descricao": "Colete ervas medicinais na floresta para o curandeiro.", "recompensa": 40},
        {"titulo": "Entrega Perigosa", "descricao": "Entregue um pacote importante atravessando o território de bandidos.", "recompensa": 60},
        {"titulo": "Tesouro Perdido", "descricao": "Encontre um tesouro perdido nas ruínas antigas.", "recompensa": 70},
        {"titulo": "Monstro da Caverna", "descricao": "Derrote o monstro que vive na caverna próxima à vila.", "recompensa": 80}
    ]
    
    import random
    missao = random.choice(missoes)
    
    # Armazenar a missão atual do jogador
    jogador.missao_atual = missao
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("Aceitar Missão", "Recusar Missão")
    
    bot.reply_to(message, f"*Missão: {missao['titulo']}*\n\n{missao['descricao']}\n\nRecompensa: {missao['recompensa']} moedas 💰\n\nDeseja aceitar esta missão?", parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text == "Aceitar Missão" and hasattr(jogadores.get(msg.from_user.id, object()), "missao_atual"))
def aceitar_missao(message):
    user_id = message.from_user.id
    jogador = jogadores[user_id]
    
    # Simular progresso da missão
    import random
    sucesso = random.random() < 0.8  # 80% de chance de sucesso
    
    if sucesso:
        # Missão concluída com sucesso
        recompensa = jogador.missao_atual["recompensa"]
        experiencia = random.randint(10, 20)
        
        jogador.moedas += recompensa
        jogador.experiencia += experiencia
        
        # Verificar se subiu de nível
        if jogador.experiencia >= jogador.nivel * 20:
            jogador.nivel += 1
            jogador.experiencia = 0
            mensagem = f"Missão *{jogador.missao_atual['titulo']}* concluída com sucesso! 🎉\n\nRecompensa: {recompensa} moedas 💰\nExperiência: {experiencia} pontos ✨\n\n*PARABÉNS! Você subiu para o nível {jogador.nivel}!* 🆙"
        else:
            mensagem = f"Missão *{jogador.missao_atual['titulo']}* concluída com sucesso! 🎉\n\nRecompensa: {recompensa} moedas 💰\nExperiência: {experiencia} pontos ✨"
        
        # Chance de encontrar um item
        if random.random() < 0.4:  # 40% de chance
            itens = ["Poção de Cura", "Espada Afiada", "Escudo Reforçado", "Arco Élfico", "Grimório Avançado", "Amuleto Mágico"]
            item = random.choice(itens)
            jogador.inventario.append(item)
            mensagem += f"\n\nVocê encontrou um item: *{item}*! 🎁"
        
        bot.reply_to(message, mensagem, parse_mode="Markdown")
        
        # Salvar jogador no banco de dados
        db.salvar_jogador(jogador)
    else:
        # Falha na missão
        bot.reply_to(message, f"Você falhou na missão *{jogador.missao_atual['titulo']}*. 😔\n\nMais sorte na próxima vez!", parse_mode="Markdown")
    
    # Remover a missão atual
    delattr(jogador, "missao_atual")

@bot.message_handler(func=lambda msg: msg.text == "Recusar Missão" and hasattr(jogadores.get(msg.from_user.id, object()), "missao_atual"))
def recusar_missao(message):
    user_id = message.from_user.id
    jogador = jogadores[user_id]
    
    bot.reply_to(message, f"Você recusou a missão *{jogador.missao_atual['titulo']}*. Volte quando estiver pronto para novas aventuras! 🗺️", parse_mode="Markdown")
    
    # Remover a missão atual
    delattr(jogador, "missao_atual")

@bot.message_handler(commands=["loja"])
def mostrar_loja(message):
    user_id = message.from_user.id
    if user_id not in jogadores:
        bot.reply_to(message, "Você ainda não iniciou o jogo! Use /start primeiro.")
        return
    
    jogador = jogadores[user_id]
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("Armas", "Armaduras")
    markup.add("Amuletos", "Poções")
    markup.add("Voltar")
    
    bot.reply_to(message, f"*Bem-vindo à Loja do Might Blade!*\n\nVocê possui {jogador.moedas} moedas 💰\n\nO que deseja ver?", parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text == "Armas")
def mostrar_armas(message):
    user_id = message.from_user.id
    jogador = jogadores[user_id]
    
    mensagem = "*Armas Disponíveis:*\n\n"
    itens_venda = []
    
    for nome, detalhes in armas.items():
        if jogador.classe == detalhes["classe"] or detalhes["classe"] == "Qualquer":
            mensagem += f"🗡️ *{nome}*\n"
            mensagem += f"Dano: {detalhes['dano']}\n"
            mensagem += f"Preço: {detalhes['preco']} moedas\n"
            mensagem += f"Descrição: {detalhes['descricao']}\n\n"
            itens_venda.append(f"Comprar {nome}")
    
    itens_venda.append("Voltar à Loja")
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for item in itens_venda:
        markup.add(item)
    
    bot.reply_to(message, mensagem, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text.startswith("Comprar "))
def comprar_item(message):
    user_id = message.from_user.id
    jogador = jogadores[user_id]
    
    # Extrair nome do item
    nome_item = message.text[8:]  # Remove "Comprar " do início
    
    # Verificar em qual categoria o item está
    item_info = None
    categoria = None
    
    if nome_item in armas:
        item_info = armas[nome_item]
        categoria = "arma"
    elif nome_item in armaduras:
        item_info = armaduras[nome_item]
        categoria = "armadura"
    elif nome_item in amuletos:
        item_info = amuletos[nome_item]
        categoria = "amuleto"
    elif nome_item in consumiveis:
        item_info = consumiveis[nome_item]
        categoria = "consumivel"
    
    if not item_info:
        bot.reply_to(message, "Item não encontrado. Tente novamente.")
        return
    
    # Verificar se o jogador tem moedas suficientes
    if jogador.moedas < item_info["preco"]:
        bot.reply_to(message, f"Você não tem moedas suficientes para comprar *{nome_item}*! Faltam {item_info['preco'] - jogador.moedas} moedas.", parse_mode="Markdown")
        return
    
    # Verificar restrições de classe
    if categoria in ["arma", "armadura"] and "classe" in item_info and item_info["classe"] != jogador.classe and item_info["classe"] != "Qualquer":
        bot.reply_to(message, f"Você não pode usar *{nome_item}* com a classe {jogador.classe}!", parse_mode="Markdown")
        return
    
    # Processo de compra
    jogador.moedas -= item_info["preco"]
    
    if categoria == "consumivel":
        jogador.inventario.append(nome_item)
        bot.reply_to(message, f"Você comprou *{nome_item}* por {item_info['preco']} moedas!\nO item foi adicionado ao seu inventário.", parse_mode="Markdown")
    elif categoria == "arma":
        # Adicionar ao equipamento ou substituir existente
        if jogador.equipamento["arma"]:
            jogador.inventario.append(jogador.equipamento["arma"])  # Guardar arma antiga no inventário
        jogador.equipamento["arma"] = nome_item
        bot.reply_to(message, f"Você comprou e equipou *{nome_item}* por {item_info['preco']} moedas!", parse_mode="Markdown")
    elif categoria == "armadura":
        # Adicionar ao equipamento ou substituir existente
        if jogador.equipamento["armadura"]:
            jogador.inventario.append(jogador.equipamento["armadura"])  # Guardar armadura antiga no inventário
        jogador.equipamento["armadura"] = nome_item
        bot.reply_to(message, f"Você comprou e equipou *{nome_item}* por {item_info['preco']} moedas!", parse_mode="Markdown")
    elif categoria == "amuleto":
        # Adicionar ao equipamento ou substituir existente
        if jogador.equipamento["amuleto"]:
            jogador.inventario.append(jogador.equipamento["amuleto"])  # Guardar amuleto antigo no inventário
        jogador.equipamento["amuleto"] = nome_item
        bot.reply_to(message, f"Você comprou e equipou *{nome_item}* por {item_info['preco']} moedas!", parse_mode="Markdown")
    
    # Salvar jogador no banco de dados após a compra
    db.salvar_jogador(jogador)

@bot.message_handler(func=lambda msg: msg.text == "Armaduras")
def mostrar_armaduras(message):
    user_id = message.from_user.id
    jogador = jogadores[user_id]
    
    mensagem = "*Armaduras Disponíveis:*\n\n"
    itens_venda = []
    
    for nome, detalhes in armaduras.items():
        if jogador.classe == detalhes["classe"] or detalhes["classe"] == "Qualquer":
            mensagem += f"🛡️ *{nome}*\n"
            mensagem += f"Defesa: {detalhes['defesa']}\n"
            if 'mana' in detalhes:
                mensagem += f"Bônus de Mana: {detalhes['mana']}\n"
            mensagem += f"Preço: {detalhes['preco']} moedas\n"
            mensagem += f"Descrição: {detalhes['descricao']}\n\n"
            itens_venda.append(f"Comprar {nome}")
    
    itens_venda.append("Voltar à Loja")
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for item in itens_venda:
        markup.add(item)
    
    bot.reply_to(message, mensagem, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text == "Poções")
def mostrar_pocoes(message):
    user_id = message.from_user.id
    jogador = jogadores[user_id]
    
    mensagem = "*Poções Disponíveis:*\n\n"
    itens_venda = []
    
    for nome, detalhes in consumiveis.items():
        if nome.startswith("Poção"):
            mensagem += f"🧪 *{nome}*\n"
            if detalhes["efeito"] == "vida":
                mensagem += f"Restaura: {detalhes['valor']} pontos de vida\n"
            elif detalhes["efeito"] == "mana":
                mensagem += f"Restaura: {detalhes['valor']} pontos de mana\n"
            elif detalhes["efeito"] == "buff":
                mensagem += f"Aumenta {detalhes['atributo']}: +{detalhes['valor']} por {detalhes['duracao']} turnos\n"
            mensagem += f"Preço: {detalhes['preco']} moedas\n"
            mensagem += f"Descrição: {detalhes['descricao']}\n\n"
            itens_venda.append(f"Comprar {nome}")
    
    itens_venda.append("Voltar à Loja")
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for item in itens_venda:
        markup.add(item)
    
    bot.reply_to(message, mensagem, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text == "Amuletos")
def mostrar_amuletos(message):
    user_id = message.from_user.id
    jogador = jogadores[user_id]
    
    mensagem = "*Amuletos Disponíveis:*\n\n"
    itens_venda = []
    
    for nome, detalhes in amuletos.items():
        if jogador.classe == detalhes["classe"] or detalhes["classe"] == "Qualquer":
            mensagem += f"🔮 *{nome}*\n"
            if detalhes["efeito"] == "defesa":
                mensagem += f"Defesa: +{detalhes['valor']}\n"
            elif detalhes["efeito"] == "sorte":
                mensagem += f"Sorte: +{detalhes['valor']}%\n"
            elif detalhes["efeito"] == "vida":
                mensagem += f"Vida: +{detalhes['valor']}\n"
            elif detalhes["efeito"] == "mana":
                mensagem += f"Mana: +{detalhes['valor']}\n"
            elif detalhes["efeito"] == "forca":
                mensagem += f"Força: +{detalhes['valor']}\n"
            else:
                mensagem += f"Efeito: {detalhes['efeito']} +{detalhes['valor']}\n"
            mensagem += f"Preço: {detalhes['preco']} moedas\n"
            mensagem += f"Descrição: {detalhes['descricao']}\n\n"
            itens_venda.append(f"Comprar {nome}")
    
    itens_venda.append("Voltar à Loja")
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for item in itens_venda:
        markup.add(item)
    
    bot.reply_to(message, mensagem, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text == "Voltar à Loja")
def voltar_loja(message):
    # Redirecionar para a função de mostrar loja
    mostrar_loja(message)

@bot.message_handler(func=lambda msg: msg.text == "Voltar")
def voltar_menu_principal(message):
    # Voltar para o menu principal
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("/perfil", "/batalha", "/missao", "/loja", "/inventario")
    bot.reply_to(message, "Voltando ao menu principal. O que deseja fazer?", reply_markup=markup)

# Sistema de inventário
@bot.message_handler(commands=["inventario"])
def comando_inventario(message):
    from inventario import mostrar_inventario
    mostrar_inventario(bot, message, jogadores)

@bot.message_handler(func=lambda msg: msg.text.startswith("Usar "))
def comando_usar_item(message):
    from inventario import usar_item
    usar_item(bot, message, jogadores, consumiveis)

@bot.message_handler(func=lambda msg: msg.text == "Equipar" and hasattr(jogadores.get(msg.from_user.id, object()), "item_selecionado"))
def comando_equipar_item(message):
    from inventario import equipar_item
    equipar_item(bot, message, jogadores, armas, armaduras, amuletos)

@bot.message_handler(func=lambda msg: msg.text == "Cancelar" and hasattr(jogadores.get(msg.from_user.id, object()), "item_selecionado"))
def comando_cancelar_equipar(message):
    user_id = message.from_user.id
    jogador = jogadores[user_id]
    
    if hasattr(jogador, "item_selecionado"):
        delattr(jogador, "item_selecionado")
    
    bot.reply_to(message, "Operação cancelada.")
    from inventario import mostrar_inventario
    mostrar_inventario(bot, message, jogadores)

# Iniciar o bot
if __name__ == "__main__":
    print("Bot iniciado!")
    bot.polling()