# Arquitetura do Might Blade Bot

Este documento descreve a arquitetura do Might Blade Bot, incluindo os componentes principais, fluxo de dados e decisões de design.

## Visão Geral

O Might Blade Bot é um bot de RPG para Telegram que permite aos jogadores criar personagens, batalhar contra monstros, coletar itens e participar de eventos globais. A arquitetura do bot foi projetada para ser modular, escalável e robusta.

## Componentes Principais

### 1. Núcleo do Bot (bot.py)

O núcleo do bot é responsável por inicializar o bot, configurar os handlers e gerenciar o ciclo de vida do bot. Ele também mantém referências globais para os jogadores ativos e o banco de dados.

### 2. Gerenciamento de Jogadores (jogador.py)

Este componente define a classe `Jogador` que representa um jogador no jogo. Ele gerencia os dados do jogador, como classe, nível, experiência, moedas, vida, ataque, defesa e inventário. Também implementa métodos para ações do jogador, como ganhar experiência, receber dano, curar, comprar itens e usar itens.

### 3. Banco de Dados (database.py)

O componente de banco de dados é responsável por persistir os dados do jogo, como jogadores, itens e eventos. Ele implementa métodos para salvar, carregar, listar e excluir jogadores. O bot utiliza MongoDB como banco de dados principal.

### 4. Comandos (comandos.py)

Este componente define os handlers para os comandos do bot, como `/start`, `/help`, `/classe`, `/moedas`, `/perfil`, `/batalha`, `/loja` e `/evento`. Cada handler é responsável por processar um comando específico e interagir com os outros componentes do bot.

### 5. Itens (itens.py)

O componente de itens define os itens disponíveis no jogo, como armas, armaduras, amuletos e consumíveis. Ele também implementa funções para obter itens por nome, listar itens por classe e aplicar efeitos de itens consumíveis.

### 6. Eventos (eventos.py)

Este componente gerencia os eventos globais do jogo, como "Chuva de Meteoros", "Eclipse Lunar" e "Festival do Guerreiro". Ele implementa funções para iniciar eventos aleatórios, verificar o fim de eventos, calcular modificadores baseados em eventos e obter informações sobre o evento atual.

### 7. Utilitários (utils.py)

O componente de utilitários fornece funções auxiliares para o bot, como limitação de taxa de requisições e tentativas automáticas para operações de banco de dados.

### 8. Tratamento de Erros (errors.py)

Este componente define classes de exceção personalizadas e funções para tratamento de erros. Ele ajuda a tornar o bot mais robusto e fornece mensagens de erro amigáveis para os usuários.

### 9. Monitoramento (monitoring.py)

O componente de monitoramento define métricas e funções para monitorar o desempenho do bot, como tempo de processamento de requisições e contagem de comandos executados. Ele utiliza o Prometheus para coletar métricas e o Grafana para visualização.

## Fluxo de Dados

1. O usuário envia um comando para o bot no Telegram.
2. O Telegram encaminha o comando para o servidor do bot.
3. O bot processa o comando usando o handler apropriado.
4. O handler interage com os componentes relevantes (jogador, banco de dados, itens, eventos).
5. O bot envia uma resposta de volta para o usuário no Telegram.

## Decisões de Design

### Modularidade

O bot foi projetado com uma arquitetura modular, onde cada componente tem uma responsabilidade específica. Isso facilita a manutenção, teste e extensão do bot.

### Robustez

O bot implementa tratamento de erros abrangente, limitação de taxa de requisições e tentativas automáticas para operações de banco de dados. Isso ajuda a tornar o bot mais robusto e resistente a falhas.

### Monitoramento

O bot utiliza o Prometheus para coletar métricas de desempenho e o Grafana para visualização. Isso permite monitorar o desempenho do bot em tempo real e identificar problemas rapidamente.

### Persistência de Dados

O bot utiliza o MongoDB para persistir os dados do jogo. O MongoDB foi escolhido por sua flexibilidade, escalabilidade e suporte a documentos JSON.

### Containerização

O bot é containerizado usando Docker e Docker Compose. Isso facilita a implantação e execução do bot em diferentes ambientes.

## Diagrama de Componentes

```
+----------------+     +----------------+     +----------------+
|                |     |                |     |                |
|   Telegram     |<--->|    Bot Core    |<--->|    Database    |
|                |     |    (bot.py)    |     | (database.py)  |
+----------------+     +----------------+     +----------------+
                              ^
                              |
                              v
+----------------+     +----------------+     +----------------+
|                |     |                |     |                |
|    Commands    |<--->|    Players     |<--->|     Items      |
|  (comandos.py) |     |  (jogador.py)  |     |   (itens.py)   |
+----------------+     +----------------+     +----------------+
        ^                     ^                      ^
        |                     |                      |
        v                     v                      v
+----------------+     +----------------+     +----------------+
|                |     |                |     |                |
|     Events     |<--->|    Utilities   |<--->|     Errors     |
|  (eventos.py)  |     |   (utils.py)   |     |  (errors.py)   |
+----------------+     +----------------+     +----------------+
                              ^
                              |
                              v
                       +----------------+
                       |                |
                       |   Monitoring   |
                       | (monitoring.py)|
                       +----------------+
```

## Conclusão

A arquitetura do Might Blade Bot foi projetada para ser modular, escalável e robusta. Ela permite que o bot seja facilmente mantido, testado e estendido. O uso de componentes bem definidos, tratamento de erros abrangente, monitoramento e containerização ajuda a garantir que o bot seja confiável e eficiente. 