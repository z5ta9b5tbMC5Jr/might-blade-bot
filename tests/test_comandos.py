import pytest
from unittest.mock import MagicMock, patch
from bot.comandos import registrar_comandos

class TestComandos:
    def test_registrar_comandos(self):
        """Testa a função registrar_comandos"""
        # Mock do objeto application
        application_mock = MagicMock()
        
        # Chamar a função
        registrar_comandos(application_mock)
        
        # Verificar se os comandos foram registrados
        assert application_mock.add_handler.call_count >= 7  # Pelo menos 7 comandos
        
    @pytest.mark.asyncio
    async def test_comando_help(self, mock_update, mock_context):
        """Testa o comando /help"""
        from bot.comandos import cmd_help
        
        # Chamar o comando
        await cmd_help(mock_update, mock_context)
        
        # Verificar se a mensagem foi enviada
        mock_context.bot.send_message.assert_called_once()
        
    @pytest.mark.asyncio
    async def test_comando_classe(self, mock_update, mock_context, mock_jogadores):
        """Testa o comando /classe"""
        from bot.comandos import cmd_classe
        
        # Configurar mock para jogador existente
        user_id = mock_update.effective_user.id
        mock_jogadores[user_id] = MagicMock()
        mock_jogadores[user_id].classe = None
        
        # Patch para acessar jogadores
        with patch('bot.comandos.jogadores', mock_jogadores):
            # Chamar o comando
            await cmd_classe(mock_update, mock_context)
            
            # Verificar se a mensagem foi enviada com os botões de classe
            mock_context.bot.send_message.assert_called_once()
            
    @pytest.mark.asyncio
    async def test_comando_moedas(self, mock_update, mock_context, mock_jogadores):
        """Testa o comando /moedas"""
        from bot.comandos import cmd_moedas
        
        # Configurar mock para jogador existente
        user_id = mock_update.effective_user.id
        mock_jogadores[user_id] = MagicMock()
        mock_jogadores[user_id].moedas = 100
        
        # Patch para acessar jogadores
        with patch('bot.comandos.jogadores', mock_jogadores):
            # Chamar o comando
            await cmd_moedas(mock_update, mock_context)
            
            # Verificar se a mensagem foi enviada com as moedas
            mock_context.bot.send_message.assert_called_once()
            
    @pytest.mark.asyncio
    async def test_comando_perfil(self, mock_update, mock_context, mock_jogadores):
        """Testa o comando /perfil"""
        from bot.comandos import cmd_perfil
        
        # Configurar mock para jogador existente
        user_id = mock_update.effective_user.id
        mock_jogadores[user_id] = MagicMock()
        mock_jogadores[user_id].to_dict.return_value = {
            "username": "testuser",
            "classe": "Guerreiro",
            "nivel": 1,
            "experiencia": 0,
            "moedas": 100,
            "vida": 100,
            "vida_maxima": 100,
            "ataque": 10,
            "defesa": 5
        }
        
        # Patch para acessar jogadores
        with patch('bot.comandos.jogadores', mock_jogadores):
            # Chamar o comando
            await cmd_perfil(mock_update, mock_context)
            
            # Verificar se a mensagem foi enviada com o perfil
            mock_context.bot.send_message.assert_called_once()
            
    @pytest.mark.asyncio
    async def test_comando_batalha(self, mock_update, mock_context, mock_jogadores):
        """Testa o comando /batalha"""
        from bot.comandos import cmd_batalha
        
        # Configurar mock para jogador existente
        user_id = mock_update.effective_user.id
        mock_jogadores[user_id] = MagicMock()
        mock_jogadores[user_id].classe = "Guerreiro"
        mock_jogadores[user_id].vida = 100
        
        # Patch para acessar jogadores
        with patch('bot.comandos.jogadores', mock_jogadores):
            # Chamar o comando
            await cmd_batalha(mock_update, mock_context)
            
            # Verificar se a mensagem foi enviada para iniciar a batalha
            mock_context.bot.send_message.assert_called_once()
            
    @pytest.mark.asyncio
    async def test_comando_loja(self, mock_update, mock_context, mock_jogadores):
        """Testa o comando /loja"""
        from bot.comandos import cmd_loja
        
        # Configurar mock para jogador existente
        user_id = mock_update.effective_user.id
        mock_jogadores[user_id] = MagicMock()
        mock_jogadores[user_id].classe = "Guerreiro"
        
        # Patch para acessar jogadores
        with patch('bot.comandos.jogadores', mock_jogadores):
            # Chamar o comando
            await cmd_loja(mock_update, mock_context)
            
            # Verificar se a mensagem foi enviada com as opções da loja
            mock_context.bot.send_message.assert_called_once()
            
    @pytest.mark.asyncio
    async def test_comando_evento(self, mock_update, mock_context):
        """Testa o comando /evento"""
        from bot.comandos import cmd_evento
        
        # Patch para obter_evento_atual
        with patch('bot.comandos.obter_evento_atual') as mock_obter_evento:
            # Configurar mock para evento ativo
            mock_obter_evento.return_value = {
                "ativo": True,
                "nome": "Chuva de Meteoros",
                "descricao": "Uma chuva de meteoros está caindo!",
                "tempo_restante": 3600,
                "fim": "01/01/2023 12:00"
            }
            
            # Chamar o comando
            await cmd_evento(mock_update, mock_context)
            
            # Verificar se a mensagem foi enviada com as informações do evento
            mock_context.bot.send_message.assert_called_once() 