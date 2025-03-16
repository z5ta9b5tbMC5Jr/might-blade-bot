# Might Blade Bot - RPG-BR

Um bot de RPG para Telegram que permite aos jogadores criar personagens, batalhar contra monstros, coletar itens, vender equipamentos e participar de eventos semanais.

**Versão Beta 1.0**  
*Desenvolvido por Bypass*

> ⚠️ Atualmente, o bot funciona apenas em chat privado. A funcionalidade para uso em grupos será adicionada em futuras atualizações.

## Funcionalidades

- **Sistema de classes** com diferentes habilidades:
  - 🗡️ **Guerreiro** - Especialista em combate corpo a corpo, alta resistência
  - 🧙 **Mago** - Domina feitiços poderosos, alto dano mágico
  - 🏹 **Arqueiro** - Mestre em ataques à distância, alta precisão

- **Sistema de batalha** contra monstros com diferentes níveis de dificuldade
  - Batalhas por turnos com diferentes mecânicas de ataque
  - Monstros adaptados ao nível do jogador
  - Possibilidade de drops de itens e moedas

- **Economia completa**:
  - 💰 Moedas para comprar equipamentos
  - 🏪 Loja com diversos itens
  - 📦 Sistema de inventário para gerenciar itens
  - 💸 Sistema de venda de itens para obter moedas

- **Eventos semanais**:
  - Diferentes eventos para cada dia da semana
  - Desafios especiais com recompensas exclusivas
  - Bônus temporários de experiência e moedas

- **Sistema de missões**:
  - Missões diárias com objetivos específicos
  - Recompensas exclusivas para missões completadas

## Comandos Disponíveis

- `/start` - Inicia o jogo e cria seu personagem
- `/help` - Mostra a lista de comandos disponíveis
- `/classe` - Escolhe ou muda a classe do personagem
- `/moedas` - Mostra suas moedas atuais
- `/perfil` - Mostra seu perfil com estatísticas detalhadas
- `/batalha` - Inicia uma batalha contra um inimigo aleatório
- `/loja` - Acessa a loja para comprar ou vender itens
- `/inventario` - Gerencia seus itens e equipamentos
- `/evento` - Mostra informações sobre o evento semanal atual
- `/missao` - Verifica suas missões atuais e progresso

## Sistema de Eventos Semanais

O Might Blade Bot possui um sistema de eventos semanais, onde cada dia da semana traz um evento especial com desafios e recompensas únicas:

- **Segunda-feira**: Dia do Guerreiro - Bônus para a classe Guerreiro
- **Terça-feira**: Dia do Mago - Bônus para a classe Mago
- **Quarta-feira**: Dia do Arqueiro - Bônus para a classe Arqueiro
- **Quinta-feira**: Caça ao Tesouro - Chance aumentada de itens raros
- **Sexta-feira**: Chuva de Moedas - Recompensas aumentadas em moedas
- **Sábado**: Festival de XP - Experiência dobrada em batalhas
- **Domingo**: Desafio dos Campeões - Inimigos mais fortes com recompensas especiais

## Sistema de Inventário e Loja

- **Inventário**:
  - Gerenciamento de equipamentos (armas, armaduras, amuletos)
  - Uso de poções e consumíveis para recuperação e buffs
  - Equipar e desequipar itens facilmente

- **Loja**:
  - Compra de itens por categoria
  - Venda de equipamentos por 60% do valor original
  - Variedade de itens específicos para cada classe

## Requisitos

- Python 3.8+
- pyTelegramBotAPI (telebot)
- SQLite3
- prometheus-client
- python-dotenv

## Instalação

1. Clone o repositório:
```
git clone https://github.com/z5ta9b5tbMC5Jr/might-blade-bot
cd might-blade-bot
```

2. Instale as dependências:
```
pip install -r requirements.txt
```

3. Crie um arquivo `.env` baseado no `.env.example` e configure o token do bot:
```
TELEGRAM_TOKEN=seu_token_aqui
```

4. Execute o bot:
```
python main.py
```

## Estrutura do Projeto

- `main.py` - Ponto de entrada principal
- `bot/` - Pacote principal do bot
  - `bot.py` - Configuração principal do bot
  - `comandos.py` - Implementação dos comandos
  - `jogador.py` - Classe para gerenciar jogadores
  - `database.py` - Operações com o banco de dados
  - `itens.py` - Definições de itens do jogo
  - `loja.py` - Sistema de loja para compra e venda
  - `inventario.py` - Gerenciamento do inventário
  - `eventos.py` - Sistema de eventos semanais
  - `missoes.py` - Sistema de missões
  - `utils.py` - Funções utilitárias
  - `errors.py` - Tratamento de erros
  - `monitoring.py` - Monitoramento com Prometheus

## Configuração do Bot no Telegram

Para configurar seu próprio bot, consulte o arquivo [SETUP.md](docs/SETUP.md) que contém instruções detalhadas sobre como criar um bot no Telegram e configurar as credenciais.

## FAQ e Guia do Usuário

Para dúvidas comuns e instruções detalhadas sobre como utilizar o bot, consulte o [Guia do Usuário](docs/GUIA_USUARIO.md) e a [FAQ](docs/FAQ.md).

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para mais detalhes. 
