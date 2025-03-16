# API do Might Blade Bot

Este documento descreve a API interna do bot Might Blade, incluindo as principais classes, funções e estruturas de dados.

## Módulos Principais

### bot.py

Módulo principal que inicializa o bot e configura os handlers.

- `iniciar_bot()`: Função principal que inicia o bot.
- `bot`: Instância global do bot.
- `jogadores`: Dicionário global que armazena os jogadores ativos.
- `db`: Instância global do banco de dados.

### jogador.py

Define a classe `Jogador` que representa um jogador no jogo.

- `Jogador`: Classe que gerencia os dados e ações de um jogador.
  - `escolher_classe(classe)`: Define a classe do jogador.
  - `ganhar_experiencia(quantidade)`: Adiciona experiência e verifica subida de nível.
  - `receber_dano(dano)`: Aplica dano ao jogador.
  - `curar(quantidade)`: Cura o jogador.
  - `comprar_item(item)`: Compra um item da loja.
  - `usar_item(item)`: Usa um item do inventário.
  - `to_dict()`: Converte o jogador para um dicionário.

### database.py

Define a classe `Database` para interação com o banco de dados.

- `Database`: Classe que gerencia a conexão e operações com o banco de dados.
  - `conectar()`: Estabelece conexão com o banco de dados.
  - `salvar_jogador(jogador)`: Salva os dados de um jogador.
  - `carregar_jogador(user_id)`: Carrega os dados de um jogador.
  - `listar_jogadores()`: Lista todos os jogadores.
  - `excluir_jogador(user_id)`: Remove um jogador do banco de dados.

### comandos.py

Define os handlers para os comandos do bot.

- `registrar_comandos(application)`: Registra todos os comandos no bot.
- `cmd_start(update, context)`: Handler para o comando /start.
- `cmd_help(update, context)`: Handler para o comando /help.
- `cmd_classe(update, context)`: Handler para o comando /classe.
- `cmd_moedas(update, context)`: Handler para o comando /moedas.
- `cmd_perfil(update, context)`: Handler para o comando /perfil.
- `cmd_batalha(update, context)`: Handler para o comando /batalha.
- `cmd_loja(update, context)`: Handler para o comando /loja.
- `cmd_evento(update, context)`: Handler para o comando /evento.

### itens.py

Define os itens disponíveis no jogo.

- `armas`: Dicionário com as armas disponíveis.
- `armaduras`: Dicionário com as armaduras disponíveis.
- `amuletos`: Dicionário com os amuletos disponíveis.
- `consumiveis`: Dicionário com os itens consumíveis.
- `obter_item_por_nome(nome)`: Retorna um item pelo nome.
- `itens_por_classe(classe)`: Retorna os itens disponíveis para uma classe.
- `aplicar_efeito_item(jogador, item)`: Aplica o efeito de um item consumível.

### eventos.py

Define o sistema de eventos globais.

- `eventos_globais`: Dicionário com os eventos disponíveis.
- `iniciar_evento_aleatorio(bot, jogadores, eventos, logger)`: Inicia um evento aleatório.
- `verificar_fim_evento(bot, jogadores, logger)`: Verifica se o evento atual terminou.
- `obter_modificador_evento(jogador, tipo, valor_base)`: Calcula o modificador de um jogador baseado no evento atual.
- `esta_ativo_evento()`: Verifica se há um evento ativo.
- `obter_evento_atual()`: Retorna informações sobre o evento atual.

### utils.py

Funções utilitárias para o bot.

- `rate_limit`: Decorador para limitar a taxa de requisições.
- `db_retry`: Decorador para tentar novamente operações de banco de dados.

### errors.py

Define classes de exceção e funções para tratamento de erros.

- `CustomError`: Classe base para exceções personalizadas.
- `DatabaseError`: Exceção para erros de banco de dados.
- `APIConnectionError`: Exceção para erros de conexão com APIs.
- `handle_error(update, context, error)`: Função para tratar erros.

### monitoring.py

Define métricas e funções para monitoramento.

- `REQUEST_TIME`: Métrica para tempo de processamento de requisições.
- `COMMAND_COUNTER`: Métrica para contagem de comandos executados.
- `monitor_requests`: Decorador para monitorar requisições.

## Estruturas de Dados

### Jogador

```python
{
    "user_id": int,
    "username": str,
    "classe": str,
    "nivel": int,
    "experiencia": int,
    "moedas": int,
    "vida": int,
    "vida_maxima": int,
    "ataque": int,
    "defesa": int,
    "inventario": {
        "armas": list,
        "armaduras": list,
        "amuletos": list,
        "consumiveis": list
    },
    "equipado": {
        "arma": dict,
        "armadura": dict,
        "amuleto": dict
    }
}
```

### Item

```python
{
    "nome": str,
    "tipo": str,  # "arma", "armadura", "amuleto", "consumivel"
    "descricao": str,
    "preco": int,
    "classes": list,  # Classes que podem usar o item
    # Atributos específicos por tipo
    "dano": int,  # Para armas
    "defesa": int,  # Para armaduras
    "efeito": dict,  # Para amuletos e consumíveis
}
```

### Evento

```python
{
    "nome": str,
    "descricao": str,
    "duracao": int,  # Em horas
    "buffs": {
        "ataque": float,
        "defesa": float,
        "experiencia": float,
        "moedas": float
    },
    "classes_afetadas": list  # Classes afetadas pelo evento
}
``` 