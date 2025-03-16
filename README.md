# Might Blade Bot

Um bot de RPG para Telegram que permite aos jogadores criar personagens, batalhar contra monstros, coletar itens e participar de eventos globais.

## Funcionalidades

- Sistema de classes (Guerreiro, Mago, Arqueiro)
- Batalhas contra monstros com sistema de combate por turnos
- Loja de itens (armas, armaduras, amuletos, consumíveis)
- Eventos globais que afetam todos os jogadores
- Sistema de perfil com estatísticas detalhadas
- Economia com moedas para comprar itens

## Comandos Disponíveis

- `/start` - Inicia o jogo
- `/help` - Mostra a lista de comandos disponíveis
- `/classe` - Escolhe a classe do personagem
- `/moedas` - Mostra suas moedas atuais
- `/perfil` - Mostra seu perfil com estatísticas detalhadas
- `/batalha` - Inicia uma batalha contra um inimigo aleatório
- `/loja` - Acessa a loja de itens
- `/evento` - Mostra informações sobre o evento global atual

## Requisitos

- Python 3.8+
- python-telegram-bot
- pymongo
- prometheus-client
- tenacity
- pyrate_limiter

## Instalação

1. Clone o repositório:
```
git clone https://github.com/seu-usuario/might-blade-bot.git
cd might-blade-bot
```

2. Instale as dependências:
```
pip install -r requirements.txt
```

3. Configure o token do bot no arquivo `.env`:
```
TELEGRAM_TOKEN=seu_token_aqui
MONGODB_URI=sua_uri_mongodb
```

4. Execute o bot:
```
python main.py
```

## Estrutura do Projeto

- `main.py` - Ponto de entrada principal
- `bot/` - Pacote principal do bot
  - `bot.py` - Núcleo do bot e configuração
  - `jogador.py` - Classe para gerenciar jogadores
  - `database.py` - Conexão e operações com o banco de dados
  - `comandos.py` - Handlers para comandos do bot
  - `itens.py` - Definições de itens do jogo
  - `eventos.py` - Sistema de eventos globais
  - `utils.py` - Funções utilitárias
  - `errors.py` - Tratamento de erros
  - `monitoring.py` - Monitoramento com Prometheus

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para mais detalhes.