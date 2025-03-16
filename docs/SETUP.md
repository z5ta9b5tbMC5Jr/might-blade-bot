# Configuração do Bot no Telegram

Este guia explica como criar um bot no Telegram e configurá-lo para uso com o Might Blade Bot.

## Criando um Novo Bot no Telegram

1. **Inicie uma conversa com o BotFather**
   - Abra o Telegram e pesquise por `@BotFather`
   - Inicie uma conversa com o BotFather clicando em "Iniciar" ou enviando `/start`

2. **Crie um novo bot**
   - Envie o comando `/newbot` para o BotFather
   - Siga as instruções para fornecer um nome para o seu bot (ex: "Meu Might Blade Bot")
   - Forneça um nome de usuário para o bot, que deve terminar com "bot" (ex: "MeuMightBladeBot" ou "meu_mighty_blade_bot")

3. **Receba o token de acesso**
   - Após criar o bot, o BotFather fornecerá um token de acesso
   - Este token é uma string longa como `7789048923:AAEgePnqXLfWB6zqzSi0xAwkcJ87XUS24QQ`
   - **IMPORTANTE**: Mantenha este token privado! Não compartilhe publicamente ou inclua em repositórios públicos

4. **Personalize seu bot (opcional)**
   - Você pode usar os comandos `/setdescription`, `/setabouttext`, e `/setuserpic` no BotFather para personalizar seu bot
   - É recomendado definir uma descrição e uma imagem para seu bot ficar mais profissional

5. **Configure comandos (opcional)**
   - Você pode definir os comandos disponíveis usando `/setcommands` no BotFather
   - Isso habilita sugestões de comandos quando os usuários digitam "/"
   - Cole a seguinte lista de comandos quando solicitado:

```
start - Iniciar o jogo e criar personagem
help - Ver lista de comandos disponíveis
classe - Escolher ou mudar a classe do personagem
moedas - Ver quantidade de moedas
perfil - Ver perfil e estatísticas do personagem
batalha - Iniciar uma batalha contra inimigos
loja - Acessar a loja para comprar e vender itens
inventario - Gerenciar itens e equipamentos
evento - Ver informações sobre evento semanal atual
missao - Verificar missões atuais e progresso
```

## Configurando o Bot no Projeto

1. **Clone o repositório**
   ```
   git clone https://github.com/z5ta9b5tbMC5Jr/might-blade-bot
   cd might-blade-bot
   ```

2. **Crie um ambiente virtual (recomendado)**
   ```
   python -m venv .venv
   
   # No Windows
   .venv\Scripts\activate
   
   # No macOS/Linux
   source .venv/bin/activate
   ```

3. **Instale as dependências**
   ```
   pip install -r requirements.txt
   ```

4. **Configure o arquivo .env**
   - Crie um arquivo `.env` na raiz do projeto
   - Adicione seu token de bot do Telegram:
   ```
   TELEGRAM_TOKEN=seu_token_aqui
   
   # Configurações de Monitoramento (opcional)
   PROMETHEUS_PORT=8000
   
   # Configurações de Logging
   LOG_LEVEL=INFO
   ```

5. **Iniciar o bot**
   ```
   python main.py
   ```

## Verificando se o Bot Está Funcionando

1. Abra o Telegram e pesquise pelo nome de usuário do seu bot
2. Inicie uma conversa enviando `/start`
3. Se o bot responder com uma mensagem de boas-vindas, a configuração foi bem-sucedida

## Resolução de Problemas Comuns

### O bot não responde
- Verifique se o token no arquivo `.env` está correto
- Certifique-se de que o bot está em execução no servidor
- Verifique os logs do bot em `bot.log` para possíveis erros

### Erro "Conflict: terminated by other getUpdates request"
- Este erro ocorre quando há mais de uma instância do bot tentando receber atualizações
- Certifique-se de que apenas uma instância do bot está em execução
- Reinicie o bot para resolver o conflito

### O bot responde lentamente
- Verifique a carga do servidor onde o bot está hospedado
- Considere otimizar as operações de banco de dados
- Verifique a conexão de internet do servidor

## Hospedagem do Bot

Para manter seu bot online 24/7, você pode hospedá-lo em:

1. **VPS/Servidor Dedicado**
   - Provedores como DigitalOcean, AWS, Google Cloud, etc.
   - Oferece controle total, mas requer mais conhecimento técnico

2. **Serviços de PaaS**
   - Plataformas como Heroku, PythonAnywhere, etc.
   - Mais fácil de configurar, mas pode ter limitações em planos gratuitos

3. **Computador pessoal**
   - Viável para testes ou uso pessoal
   - Não recomendado para produção devido à disponibilidade limitada

## Segurança

1. **Nunca compartilhe seu token de bot**
   - O token dá acesso completo ao seu bot
   - Não o inclua em repositórios públicos ou compartilhe em mensagens

2. **Tenha cuidado com os comandos disponíveis**
   - Implemente limitações de rate (já incluídas neste bot)
   - Verifique as entradas do usuário para evitar injeções

3. **Mantenha seu bot atualizado**
   - Atualize regularmente as dependências para corrigir vulnerabilidades
   - Monitore os logs para detectar problemas ou abusos 
