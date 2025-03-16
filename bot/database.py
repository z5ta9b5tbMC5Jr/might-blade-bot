import sqlite3
import json
import logging
from .errors import DatabaseError
from .utils import db_retry

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_file="rpg_database.db"):
        self.db_file = db_file
        self.conn = None
        self.create_tables()
    
    @db_retry
    def connect(self):
        """Conecta ao banco de dados com retry automático em caso de falha"""
        try:
            self.conn = sqlite3.connect(self.db_file)
            return self.conn
        except sqlite3.Error as e:
            error_msg = f"Erro ao conectar ao banco de dados: {e}"
            logger.error(error_msg)
            raise DatabaseError(error_msg)
    
    def create_tables(self):
        """Cria as tabelas necessárias para o jogo"""
        try:
            conn = self.connect()
            if not conn:
                logger.error("Não foi possível conectar ao banco de dados para criar tabelas")
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
            
            # Tabela para logs de atividade
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs_atividade (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                jogador_id INTEGER,
                acao TEXT,
                timestamp TEXT,
                detalhes TEXT,
                FOREIGN KEY (jogador_id) REFERENCES jogadores (id)
            )
            ''')
            
            # Tabela para estatísticas
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS estatisticas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                jogador_id INTEGER,
                batalhas_vencidas INTEGER DEFAULT 0,
                batalhas_perdidas INTEGER DEFAULT 0,
                missoes_completadas INTEGER DEFAULT 0,
                missoes_falhadas INTEGER DEFAULT 0,
                moedas_ganhas INTEGER DEFAULT 0,
                moedas_gastas INTEGER DEFAULT 0,
                FOREIGN KEY (jogador_id) REFERENCES jogadores (id)
            )
            ''')
            
            # Tabela para eventos
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS eventos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                data_inicio TEXT,
                data_fim TEXT,
                status TEXT DEFAULT 'ativo',
                detalhes TEXT
            )
            ''')
            
            # Tabela para participações em eventos
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS participacoes_evento (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                jogador_id INTEGER,
                evento_id INTEGER,
                vitorias INTEGER DEFAULT 0,
                recompensa_recebida INTEGER DEFAULT 0,
                FOREIGN KEY (jogador_id) REFERENCES jogadores (id),
                FOREIGN KEY (evento_id) REFERENCES eventos (id)
            )
            ''')
            
            conn.commit()
            logger.info("Tabelas criadas com sucesso")
        except sqlite3.Error as e:
            logger.error(f"Erro ao criar tabelas: {e}", exc_info=True)
            if conn:
                conn.rollback()
        finally:
            if conn:
                conn.close()
    
    @db_retry
    def salvar_jogador(self, jogador):
        """Salva os dados do jogador no banco de dados"""
        try:
            conn = self.connect()
            if not conn:
                logger.error("Não foi possível conectar ao banco de dados para salvar jogador")
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
                jogador.user_id, 
                jogador.username, 
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
            error_msg = f"Erro ao salvar jogador: {e}"
            logger.error(error_msg, exc_info=True)
            if conn:
                conn.rollback()
            raise DatabaseError(error_msg)
        finally:
            if conn:
                conn.close()
    
    @db_retry
    def carregar_jogador(self, jogador_id):
        """Carrega os dados do jogador do banco de dados"""
        try:
            conn = self.connect()
            if not conn:
                logger.error("Não foi possível conectar ao banco de dados para carregar jogador")
                return None
                
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM jogadores WHERE id = ?', (jogador_id,))
            dados = cursor.fetchone()
            
            if dados:
                try:
                    from .jogador import Jogador
                    
                    # Criar objeto jogador a partir dos dados
                    jogador = Jogador(
                        user_id=dados[0],
                        username=dados[1],
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
                    logger.error(f"Erro ao processar dados do jogador: {e}", exc_info=True)
                    return None
            
            return None
        except sqlite3.Error as e:
            error_msg = f"Erro ao carregar jogador: {e}"
            logger.error(error_msg, exc_info=True)
            raise DatabaseError(error_msg)
        finally:
            if conn:
                conn.close()
    
    def registrar_atividade(self, jogador_id, acao, detalhes=None):
        """Registra atividade do jogador para análise e depuração"""
        try:
            import datetime
            conn = self.connect()
            if not conn:
                logger.error("Não foi possível conectar ao banco de dados para registrar atividade")
                return False
                
            cursor = conn.cursor()
            
            timestamp = datetime.datetime.now().isoformat()
            detalhes_json = json.dumps(detalhes) if detalhes else None
            
            cursor.execute('''
            INSERT INTO logs_atividade (jogador_id, acao, timestamp, detalhes)
            VALUES (?, ?, ?, ?)
            ''', (jogador_id, acao, timestamp, detalhes_json))
            
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Erro ao registrar atividade: {e}", exc_info=True)
            if conn:
                conn.rollback()
            return False
        finally:
            if conn:
                conn.close()
    
    def atualizar_estatisticas(self, jogador_id, campo, valor=1):
        """Atualiza estatísticas do jogador"""
        try:
            conn = self.connect()
            if not conn:
                logger.error("Não foi possível conectar ao banco de dados para atualizar estatísticas")
                return False
                
            cursor = conn.cursor()
            
            # Verificar se registro já existe
            cursor.execute('SELECT id FROM estatisticas WHERE jogador_id = ?', (jogador_id,))
            if not cursor.fetchone():
                cursor.execute('INSERT INTO estatisticas (jogador_id) VALUES (?)', (jogador_id,))
            
            # Atualizar campo específico
            cursor.execute(f'''
            UPDATE estatisticas SET {campo} = {campo} + ? WHERE jogador_id = ?
            ''', (valor, jogador_id))
            
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Erro ao atualizar estatísticas: {e}", exc_info=True)
            if conn:
                conn.rollback()
            return False
        finally:
            if conn:
                conn.close()
    
    @db_retry
    def registrar_evento_atual(self, nome_evento, data_fim):
        """Registra um novo evento no banco de dados"""
        try:
            conn = self.connect()
            if not conn:
                logger.error("Não foi possível conectar ao banco de dados para registrar evento")
                return False
                
            cursor = conn.cursor()
            
            # Marcar eventos anteriores como finalizados
            cursor.execute('''
            UPDATE eventos SET status = 'finalizado'
            WHERE status = 'ativo'
            ''')
            
            # Inserir novo evento
            data_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute('''
            INSERT INTO eventos (nome, data_inicio, data_fim, status)
            VALUES (?, ?, ?, 'ativo')
            ''', (nome_evento, data_atual, data_fim))
            
            evento_id = cursor.lastrowid
            
            conn.commit()
            logger.info(f"Evento {nome_evento} registrado com sucesso, ID: {evento_id}")
            return evento_id
            
        except sqlite3.Error as e:
            error_msg = f"Erro ao registrar evento: {e}"
            logger.error(error_msg, exc_info=True)
            if conn:
                conn.rollback()
            raise DatabaseError(error_msg)
        finally:
            if conn:
                conn.close()
    
    @db_retry
    def finalizar_evento_atual(self):
        """Finaliza o evento ativo atual"""
        try:
            conn = self.connect()
            if not conn:
                logger.error("Não foi possível conectar ao banco de dados para finalizar evento")
                return False
                
            cursor = conn.cursor()
            
            # Marcar evento ativo como finalizado
            cursor.execute('''
            UPDATE eventos SET status = 'finalizado'
            WHERE status = 'ativo'
            ''')
            
            if cursor.rowcount > 0:
                logger.info("Evento atual finalizado com sucesso")
            else:
                logger.warning("Nenhum evento ativo encontrado para finalizar")
            
            conn.commit()
            return True
            
        except sqlite3.Error as e:
            error_msg = f"Erro ao finalizar evento: {e}"
            logger.error(error_msg, exc_info=True)
            if conn:
                conn.rollback()
            raise DatabaseError(error_msg)
        finally:
            if conn:
                conn.close()
    
    @db_retry
    def registrar_participacao_evento(self, jogador_id, evento_id):
        """Registra a participação de um jogador em um evento"""
        try:
            conn = self.connect()
            if not conn:
                logger.error("Não foi possível conectar ao banco de dados para registrar participação em evento")
                return False
                
            cursor = conn.cursor()
            
            # Verificar se já existe participação
            cursor.execute('''
            SELECT id FROM participacoes_evento
            WHERE jogador_id = ? AND evento_id = ?
            ''', (jogador_id, evento_id))
            
            if cursor.fetchone():
                # Já existe participação, não fazer nada
                logger.info(f"Jogador {jogador_id} já está participando do evento {evento_id}")
                return True
            
            # Inserir nova participação
            cursor.execute('''
            INSERT INTO participacoes_evento (jogador_id, evento_id, vitorias)
            VALUES (?, ?, 0)
            ''', (jogador_id, evento_id))
            
            conn.commit()
            logger.info(f"Participação do jogador {jogador_id} no evento {evento_id} registrada com sucesso")
            return True
            
        except sqlite3.Error as e:
            error_msg = f"Erro ao registrar participação em evento: {e}"
            logger.error(error_msg, exc_info=True)
            if conn:
                conn.rollback()
            raise DatabaseError(error_msg)
        finally:
            if conn:
                conn.close()
    
    @db_retry
    def registrar_vitoria_evento(self, jogador_id, evento_id):
        """Incrementa o número de vitórias de um jogador em um evento"""
        try:
            conn = self.connect()
            if not conn:
                logger.error("Não foi possível conectar ao banco de dados para registrar vitória em evento")
                return False
                
            cursor = conn.cursor()
            
            # Verificar se existe participação
            cursor.execute('''
            SELECT id FROM participacoes_evento
            WHERE jogador_id = ? AND evento_id = ?
            ''', (jogador_id, evento_id))
            
            if not cursor.fetchone():
                # Não existe participação, criar uma
                cursor.execute('''
                INSERT INTO participacoes_evento (jogador_id, evento_id, vitorias)
                VALUES (?, ?, 1)
                ''', (jogador_id, evento_id))
            else:
                # Incrementar vitórias
                cursor.execute('''
                UPDATE participacoes_evento
                SET vitorias = vitorias + 1
                WHERE jogador_id = ? AND evento_id = ?
                ''', (jogador_id, evento_id))
            
            conn.commit()
            logger.info(f"Vitória do jogador {jogador_id} no evento {evento_id} registrada com sucesso")
            return True
            
        except sqlite3.Error as e:
            error_msg = f"Erro ao registrar vitória em evento: {e}"
            logger.error(error_msg, exc_info=True)
            if conn:
                conn.rollback()
            raise DatabaseError(error_msg)
        finally:
            if conn:
                conn.close()
    
    @db_retry
    def obter_evento_ativo(self):
        """Retorna informações sobre o evento ativo atual"""
        try:
            conn = self.connect()
            if not conn:
                logger.error("Não foi possível conectar ao banco de dados para obter evento ativo")
                return None
                
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT id, nome, data_inicio, data_fim, detalhes
            FROM eventos
            WHERE status = 'ativo'
            ORDER BY id DESC
            LIMIT 1
            ''')
            
            resultado = cursor.fetchone()
            
            if resultado:
                return {
                    "id": resultado[0],
                    "nome": resultado[1],
                    "data_inicio": resultado[2],
                    "data_fim": resultado[3],
                    "detalhes": resultado[4]
                }
            
            return None
            
        except sqlite3.Error as e:
            error_msg = f"Erro ao obter evento ativo: {e}"
            logger.error(error_msg, exc_info=True)
            raise DatabaseError(error_msg)
        finally:
            if conn:
                conn.close()
    
    @db_retry
    def obter_participantes_evento(self, evento_id):
        """Retorna lista de participantes de um evento"""
        try:
            conn = self.connect()
            if not conn:
                logger.error("Não foi possível conectar ao banco de dados para obter participantes do evento")
                return []
                
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT jogador_id, vitorias, recompensa_recebida
            FROM participacoes_evento
            WHERE evento_id = ?
            ''', (evento_id,))
            
            resultados = cursor.fetchall()
            
            participantes = []
            for resultado in resultados:
                participantes.append({
                    "jogador_id": resultado[0],
                    "vitorias": resultado[1],
                    "recompensa_recebida": resultado[2] == 1
                })
            
            return participantes
            
        except sqlite3.Error as e:
            error_msg = f"Erro ao obter participantes do evento: {e}"
            logger.error(error_msg, exc_info=True)
            raise DatabaseError(error_msg)
        finally:
            if conn:
                conn.close() 