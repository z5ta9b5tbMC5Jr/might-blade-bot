# Contribuindo para o Might Blade Bot

Obrigado pelo seu interesse em contribuir para o Might Blade Bot! Este documento fornece diretrizes para contribuir com o projeto.

## Como Contribuir

### Reportando Bugs

Se você encontrar um bug, por favor, crie uma issue no GitHub com as seguintes informações:

1. Título claro e descritivo
2. Passos detalhados para reproduzir o bug
3. Comportamento esperado
4. Comportamento atual
5. Capturas de tela (se aplicável)
6. Informações do ambiente (sistema operacional, versão do Python, etc.)

### Sugerindo Melhorias

Se você tem uma ideia para melhorar o bot, por favor, crie uma issue no GitHub com as seguintes informações:

1. Título claro e descritivo
2. Descrição detalhada da melhoria
3. Justificativa para a melhoria
4. Exemplos de como a melhoria seria usada (se aplicável)

### Enviando Pull Requests

1. Faça um fork do repositório
2. Clone o seu fork: `git clone https://github.com/seu-usuario/might-blade-bot.git`
3. Crie uma branch para a sua feature: `git checkout -b feature/nome-da-feature`
4. Faça suas alterações
5. Execute os testes: `pytest`
6. Commit suas alterações: `git commit -m "Adiciona nova feature"`
7. Push para a branch: `git push origin feature/nome-da-feature`
8. Abra um Pull Request no GitHub

## Diretrizes de Código

### Estilo de Código

- Siga o [PEP 8](https://www.python.org/dev/peps/pep-0008/) para código Python
- Use docstrings no formato [Google Style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- Mantenha linhas com no máximo 100 caracteres
- Use nomes descritivos para variáveis, funções e classes
- Escreva comentários para código complexo

### Testes

- Escreva testes para todas as novas funcionalidades
- Mantenha a cobertura de testes acima de 80%
- Execute os testes antes de enviar um Pull Request: `pytest`

### Documentação

- Atualize a documentação para refletir as alterações feitas
- Documente novas funcionalidades com exemplos de uso
- Mantenha o README.md atualizado

## Estrutura do Projeto

```
might-blade-bot/
├── bot/                  # Pacote principal do bot
│   ├── __init__.py       # Torna a pasta um pacote Python
│   ├── bot.py            # Núcleo do bot
│   ├── jogador.py        # Classe para gerenciar jogadores
│   ├── database.py       # Conexão e operações com o banco de dados
│   ├── comandos.py       # Handlers para comandos do bot
│   ├── itens.py          # Definições de itens do jogo
│   ├── eventos.py        # Sistema de eventos globais
│   ├── utils.py          # Funções utilitárias
│   ├── errors.py         # Tratamento de erros
│   └── monitoring.py     # Monitoramento com Prometheus
├── tests/                # Testes automatizados
│   ├── __init__.py       # Torna a pasta um pacote Python
│   ├── conftest.py       # Configuração para testes
│   ├── test_jogador.py   # Testes para a classe Jogador
│   ├── test_itens.py     # Testes para o módulo de itens
│   ├── test_eventos.py   # Testes para o módulo de eventos
│   └── test_comandos.py  # Testes para os comandos do bot
├── docs/                 # Documentação
│   ├── API.md            # Documentação da API
│   ├── ARQUITETURA.md    # Documentação da arquitetura
│   └── CONTRIBUINDO.md   # Guia de contribuição
├── main.py               # Ponto de entrada principal
├── requirements.txt      # Dependências do projeto
├── .env.example          # Exemplo de arquivo de configuração
├── Dockerfile            # Configuração do Docker
├── docker-compose.yml    # Configuração do Docker Compose
├── prometheus.yml        # Configuração do Prometheus
├── pytest.ini           # Configuração do pytest
├── .gitignore           # Arquivos a serem ignorados pelo Git
├── LICENSE              # Licença do projeto
└── README.md            # Documentação principal
```

## Fluxo de Trabalho

1. Escolha uma issue para trabalhar ou crie uma nova
2. Discuta a abordagem na issue
3. Implemente a solução
4. Escreva testes
5. Atualize a documentação
6. Envie um Pull Request
7. Responda aos comentários de revisão
8. Aguarde a aprovação e merge

## Código de Conduta

Por favor, seja respeitoso e construtivo em todas as interações. Não toleramos comportamento abusivo, ofensivo ou discriminatório.

## Licença

Ao contribuir para este projeto, você concorda que suas contribuições serão licenciadas sob a mesma licença do projeto (MIT). 