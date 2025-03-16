import logging

logger = logging.getLogger(__name__)

class Jogador:
    def __init__(self, user_id, username, classe=None, moedas=100):
        self.user_id = user_id
        self.username = username
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
        
        # Buffs ativos
        self.buffs = []
        
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
        """Aumenta o nível do jogador e ajusta seus atributos"""
        try:
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
            
            logger.info(f"Jogador {self.user_id} ({self.username}) subiu para o nível {self.nivel}")
            return True, f"Você subiu para o nível {self.nivel}!"
        except Exception as e:
            logger.error(f"Erro ao subir de nível: {e}", exc_info=True)
            return False, "Ocorreu um erro ao subir de nível"
    
    def adicionar_experiencia(self, valor):
        """Adiciona experiência ao jogador e verifica se subiu de nível"""
        try:
            self.experiencia += valor
            
            # Verificar se subiu de nível (experiência necessária = nível * 20)
            if self.experiencia >= self.nivel * 20:
                return self.subir_nivel()
            
            return False, None
        except Exception as e:
            logger.error(f"Erro ao adicionar experiência: {e}", exc_info=True)
            return False, "Ocorreu um erro ao adicionar experiência"
    
    def usar_habilidade(self, habilidade_nome):
        """Usa uma habilidade do jogador se ele tiver mana suficiente"""
        try:
            if habilidade_nome not in self.habilidades:
                return False, "Você não possui essa habilidade!"
            
            # Dicionário com informações das habilidades: custo de mana e mensagem
            habilidades_info = {
                "Golpe Poderoso": {"mana": 10, "mensagem": f"*{self.username}* usou *Golpe Poderoso*! 💪"},
                "Escudo Protetor": {"mana": 5, "mensagem": f"*{self.username}* usou *Escudo Protetor*! 🛡️"},
                "Bola de Fogo": {"mana": 15, "mensagem": f"*{self.username}* lançou *Bola de Fogo*! 🔥"},
                "Escudo Arcano": {"mana": 10, "mensagem": f"*{self.username}* usou *Escudo Arcano*! 🧙"},
                "Grito de Guerra": {"mana": 12, "mensagem": f"*{self.username}* usou *Grito de Guerra*! 🔊"},
                "Raio Elétrico": {"mana": 18, "mensagem": f"*{self.username}* lançou *Raio Elétrico*! ⚡"},
                "Chuva de Flechas": {"mana": 15, "mensagem": f"*{self.username}* usou *Chuva de Flechas*! 🏹"},
                "Disparo Múltiplo": {"mana": 12, "mensagem": f"*{self.username}* usou *Disparo Múltiplo*! 🏹"},
                "Tiro Certeiro": {"mana": 8, "mensagem": f"*{self.username}* usou *Tiro Certeiro*! 🎯"}
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
        except Exception as e:
            logger.error(f"Erro ao usar habilidade: {e}", exc_info=True)
            return False, "Ocorreu um erro ao usar a habilidade"
    
    def adicionar_item(self, item):
        """Adiciona um item ao inventário do jogador"""
        try:
            self.inventario.append(item)
            return True
        except Exception as e:
            logger.error(f"Erro ao adicionar item ao inventário: {e}", exc_info=True)
            return False
    
    def remover_item(self, item):
        """Remove um item do inventário do jogador"""
        try:
            if item in self.inventario:
                self.inventario.remove(item)
                return True
            return False
        except Exception as e:
            logger.error(f"Erro ao remover item do inventário: {e}", exc_info=True)
            return False
    
    def equipar_item(self, item, tipo):
        """Equipa um item no jogador"""
        try:
            # Verificar se o item está no inventário
            if item not in self.inventario:
                return False, "Você não possui esse item no inventário"
            
            # Guardar item atual no inventário (se existir)
            item_atual = self.equipamento.get(tipo)
            if item_atual:
                self.inventario.append(item_atual)
            
            # Equipar novo item
            self.equipamento[tipo] = item
            self.inventario.remove(item)
            
            return True, f"Você equipou {item}!"
        except Exception as e:
            logger.error(f"Erro ao equipar item: {e}", exc_info=True)
            return False, "Ocorreu um erro ao equipar o item"
    
    def aplicar_buff(self, buff):
        """Aplica um buff temporário ao jogador"""
        try:
            self.buffs.append(buff)
            
            # Aplicar efeito do buff
            if buff["atributo"] == "forca":
                self.forca += buff["valor"]
            elif buff["atributo"] == "destreza":
                self.destreza += buff["valor"]
            elif buff["atributo"] == "inteligencia":
                self.inteligencia += buff["valor"]
            elif buff["atributo"] == "todos":
                self.forca += buff["valor"]
                self.destreza += buff["valor"]
                self.inteligencia += buff["valor"]
            
            return True
        except Exception as e:
            logger.error(f"Erro ao aplicar buff: {e}", exc_info=True)
            return False
    
    def atualizar_buffs(self):
        """Atualiza os buffs ativos e remove os expirados"""
        try:
            buffs_ativos = []
            
            for buff in self.buffs:
                buff["duracao"] -= 1
                
                # Se ainda tiver duração, manter o buff
                if buff["duracao"] > 0:
                    buffs_ativos.append(buff)
                else:
                    # Remover efeito do buff ao expirar
                    if buff["atributo"] == "forca":
                        self.forca -= buff["valor"]
                    elif buff["atributo"] == "destreza":
                        self.destreza -= buff["valor"]
                    elif buff["atributo"] == "inteligencia":
                        self.inteligencia -= buff["valor"]
                    elif buff["atributo"] == "todos":
                        self.forca -= buff["valor"]
                        self.destreza -= buff["valor"]
                        self.inteligencia -= buff["valor"]
            
            self.buffs = buffs_ativos
            return True
        except Exception as e:
            logger.error(f"Erro ao atualizar buffs: {e}", exc_info=True)
            return False
    
    def __str__(self):
        """Retorna uma representação em string do jogador para depuração"""
        return f"Jogador(user_id={self.user_id}, username={self.username}, classe={self.classe}, nivel={self.nivel})" 