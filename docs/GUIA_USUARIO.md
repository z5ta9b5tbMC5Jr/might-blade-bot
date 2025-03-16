# Guia do Usuário - Might Blade Bot

Este guia prático ensina como jogar o Might Blade Bot, um jogo de RPG pelo Telegram. Aqui você encontrará explicações detalhadas sobre todas as funcionalidades e mecânicas do jogo.

## Índice
1. [Primeiros Passos](#primeiros-passos)
2. [Escolhendo sua Classe](#escolhendo-sua-classe)
3. [Combate e Batalhas](#combate-e-batalhas)
4. [Gerenciando seu Inventário](#gerenciando-seu-inventário)
5. [Loja e Economia](#loja-e-economia)
6. [Eventos Semanais](#eventos-semanais)
7. [Sistema de Missões](#sistema-de-missões)
8. [Evolução do Personagem](#evolução-do-personagem)
9. [Botões e Navegação](#botões-e-navegação)
10. [Dicas Avançadas](#dicas-avançadas)

## Primeiros Passos

### Iniciando o Jogo
1. Abra o Telegram e pesquise pelo nome do bot
2. Inicie uma conversa e envie o comando `/start`
3. Siga as instruções iniciais para criar seu personagem
4. Use `/help` a qualquer momento para ver os comandos disponíveis

### Interface Principal
Após iniciar o jogo, você terá acesso a todos os comandos. Os principais são:
- `/batalha` - Enfrente inimigos
- `/loja` - Compre e venda itens
- `/inventario` - Gerencie seus equipamentos
- `/perfil` - Veja seus status e progresso
- `/evento` - Informações sobre evento atual
- `/missao` - Verifique sua missão atual

## Escolhendo sua Classe

No Might Blade Bot, você pode escolher entre três classes, cada uma com características únicas:

### Guerreiro 🗡️
- **Especialidade**: Combate corpo a corpo
- **Pontos Fortes**: Alta vida, dano físico consistente
- **Habilidades**: Golpe Poderoso, Postura Defensiva
- **Ideal para**: Jogadores que preferem confronto direto e resistência

### Mago 🧙
- **Especialidade**: Magias e dano à distância
- **Pontos Fortes**: Alto dano em área, manipulação de elementos
- **Habilidades**: Bola de Fogo, Raio Arcano
- **Ideal para**: Jogadores estratégicos que preferem grande poder de ataque

### Arqueiro 🏹
- **Especialidade**: Ataques precisos à distância
- **Pontos Fortes**: Precisão, chance de crítico, esquiva
- **Habilidades**: Tiro Preciso, Chuva de Flechas
- **Ideal para**: Jogadores que valorizam agilidade e golpes críticos

### Como escolher ou mudar de classe
- Use o comando `/classe` para escolher sua classe inicial
- Você pode mudar de classe posteriormente com o mesmo comando, mas perderá parte do progresso

## Combate e Batalhas

### Iniciando uma Batalha
1. Use o comando `/batalha` para encontrar um inimigo
2. O sistema escolherá automaticamente um inimigo adequado ao seu nível
3. A batalha ocorre em turnos alternados entre você e o inimigo

### Durante o Combate
Em seu turno, você pode:
- **Atacar**: Causa dano baseado em sua arma e atributos
- **Usar Habilidade**: Cada classe tem habilidades especiais que consomem mana
- **Usar Item**: Utilizar poções ou outros consumíveis do inventário
- **Fugir**: Encerrar a batalha sem recompensas (às vezes pode falhar)

### Resultado da Batalha
- **Vitória**: Você ganha experiência, moedas e possivelmente itens
- **Derrota**: Você não recebe recompensas, mas não há outras penalidades
- O progresso em missões é atualizado automaticamente após cada batalha

## Gerenciando seu Inventário

Para acessar seu inventário, use o comando `/inventario`. No inventário você pode:

### Visualizar Itens
Seus itens são organizados por categorias:
- 🗡️ **Armas**
- 🛡️ **Armaduras**
- 📿 **Amuletos**
- 🧪 **Poções**
- 📦 **Outros itens**

### Equipar Itens
1. Selecione o item no inventário
2. Escolha "Equipar"
3. O item substituirá qualquer equipamento atual da mesma categoria
4. O item substituído voltará automaticamente para o inventário

### Usar Consumíveis
1. Selecione uma poção ou consumível
2. Escolha "Usar"
3. Os efeitos são aplicados imediatamente
4. Poções de vida recuperam pontos de vida
5. Poções de mana recuperam pontos de mana
6. Poções de buff dão bônus temporários

## Loja e Economia

### Acessando a Loja
Use o comando `/loja` para acessar a loja. Na loja você pode comprar e vender itens.

### Comprando Itens
1. Selecione a categoria desejada (Armas, Armaduras, Amuletos ou Poções)
2. Escolha o item que deseja comprar
3. Confirme a compra
4. Armas, armaduras e amuletos são equipados automaticamente
5. Consumíveis vão para o inventário

### Vendendo Itens
1. Na loja, selecione "💰 Vender Itens"
2. Escolha qual item deseja vender
3. Confirme a venda
4. Você receberá 60% do valor original do item em moedas
5. Lembre-se: não é possível vender itens equipados!

### Gerenciando Moedas
Para ver sua quantidade atual de moedas, use `/moedas` ou `/perfil`.
Formas de ganhar moedas:
- Derrotar inimigos em batalhas
- Vender itens na loja
- Completar missões
- Participar de eventos especiais

## Eventos Semanais

O Might Blade Bot possui um sistema de eventos semanais, onde cada dia tem um evento especial:

### Calendário de Eventos
- **Segunda-feira**: Dia do Guerreiro
  - Bônus para guerreiros: +15% de dano físico
  - Chance aumentada de encontrar armas para guerreiros

- **Terça-feira**: Dia do Mago
  - Bônus para magos: +20% de dano mágico
  - Chance aumentada de encontrar itens mágicos

- **Quarta-feira**: Dia do Arqueiro
  - Bônus para arqueiros: +25% de chance de crítico
  - Chance aumentada de encontrar equipamentos de arqueiro

- **Quinta-feira**: Caça ao Tesouro
  - Chance aumentada de encontrar itens raros
  - Drops de melhor qualidade em todas as batalhas

- **Sexta-feira**: Chuva de Moedas
  - Ganho de moedas aumentado em 50%
  - Preços reduzidos na loja

- **Sábado**: Festival de XP
  - Experiência ganha em batalhas dobrada
  - Encontros com inimigos especiais que dão mais XP

- **Domingo**: Desafio dos Campeões
  - Encontro com inimigos mais fortes
  - Recompensas triplicadas por vitória

### Verificando o Evento Atual
Use o comando `/evento` para ver detalhes sobre o evento em andamento.

## Sistema de Missões

O sistema de missões oferece objetivos diários para cumprir e ganhar recompensas especiais.

### Como Acessar Missões
Use o comando `/missao` para ver sua missão atual, progresso e recompensas.

### Tipos de Missões
- **Caça**: Derrotar determinado número de inimigos
- **Coleta**: Obter itens específicos
- **Economia**: Gastar ou acumular moedas
- **Exploração**: Completar determinado número de batalhas

### Recompensas de Missões
As recompensas podem incluir:
- Moedas
- Itens especiais
- Pontos de experiência
- Poções raras

### Progresso das Missões
- O progresso é atualizado automaticamente após batalhas e outras ações
- Use `/missao` para verificar seu progresso atual
- Quando completar uma missão, use o comando novamente para receber a recompensa

## Evolução do Personagem

### Sistema de Níveis
- Ganhe experiência (XP) derrotando inimigos e completando missões
- Ao acumular XP suficiente, seu personagem sobe de nível
- Cada nível aumenta seus atributos base e desbloqueia inimigos mais desafiadores

### Atributos do Personagem
- **Vida**: Determina quanto dano você pode receber
- **Mana**: Recurso para usar habilidades especiais
- **Ataque**: Influencia o dano de ataques físicos
- **Defesa**: Reduz o dano recebido
- **Inteligência**: Aumenta o dano mágico e reserva de mana
- **Agilidade**: Afeta precisão, esquiva e críticos

### Equipamentos
Equipamentos são essenciais para aumentar seus atributos:
- **Armas**: Aumentam principalmente o ataque
- **Armaduras**: Aumentam principalmente a defesa
- **Amuletos**: Fornecem bônus variados (vida, mana, sorte, etc.)

## Botões e Navegação

O Might Blade Bot usa botões interativos para facilitar a navegação:

### Teclados Personalizados
- Muitos comandos mostram botões específicos para facilitar sua interação
- Toque nos botões para escolher opções mais rapidamente
- Você sempre pode voltar digitando comandos manualmente

### Navegação Padrão
- "🔙 Voltar" - Retorna ao menu anterior
- "🔙 Voltar à Loja" - Retorna ao menu principal da loja
- "📦 Ver Inventário" - Acesso rápido ao inventário

## Dicas Avançadas

### Otimizando seu Personagem
- Foque em equipamentos que complementam sua classe
- Guarde poções para situações difíceis
- Participe dos eventos que beneficiam sua classe

### Economia de Recursos
- Venda equipamentos que não usa para ganhar moedas extras
- Invista em equipamentos duráveis antes de comprar consumíveis
- Complete missões diariamente para ganhos constantes

### Combate Eficiente
- Guerreiros devem focar em equipamentos de defesa e ataque físico
- Magos devem priorizar itens que aumentam mana e inteligência
- Arqueiros devem investir em itens de precisão e crítico

### Explorando Eventos
- Cada evento favorece diferentes estratégias de jogo
- Aproveite a "Chuva de Moedas" para fazer compras grandes
- Use o "Festival de XP" para subir de nível rapidamente 