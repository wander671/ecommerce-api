# 🛒 E-commerce API

API REST para um sistema de e-commerce, construída como projeto de estudo com evolução progressiva de arquitetura — do nível estágio ao sênior.

## 📌 Status atual: Nível Pleno (em andamento) 🚧

CRUD de produtos e categorias com persistência em PostgreSQL, cadastro de usuários, login com token JWT e a primeira rota protegida.

> ⚠️ As rotas de escrita de produtos e categorias (criar, alterar, apagar) ainda **não exigem login**. Protegê-las é o próximo passo do roadmap.

## 🚀 Tecnologias

- **[FastAPI](https://fastapi.tiangolo.com/)** — framework web em Python
- **[Pydantic](https://docs.pydantic.dev/)** — validação de dados e configurações
- **[SQLAlchemy](https://www.sqlalchemy.org/)** — ORM para comunicação com o banco de dados
- **[PostgreSQL](https://www.postgresql.org/)** — banco de dados relacional
- **[Docker](https://www.docker.com/)** — containerização do banco de dados
- **[Poetry](https://python-poetry.org/)** — gerenciamento de dependências
- **[bcrypt](https://pypi.org/project/bcrypt/)** — hash seguro de senhas
- **[python-jose](https://pypi.org/project/python-jose/)** — geração e conferência de tokens JWT

## 📋 Funcionalidades

**Produtos**
- ✅ Listar produtos
- ✅ Buscar produto por ID
- ✅ Criar produto
- ✅ Atualizar produto (parcialmente)
- ✅ Deletar produto

**Categorias**
- ✅ Modelagem com relacionamento 1:N (uma categoria possui vários produtos)
- ✅ Listar, buscar, criar, atualizar e deletar categorias
- ✅ Nome de categoria único (conflito retorna 409 com mensagem clara)
- ✅ Validação: produto só pode ser criado com categoria existente
- ✅ Bloqueio de exclusão de categoria com produtos (retorna 409)

**Usuários e autenticação**
- ✅ Cadastro de usuário (`POST /users`), com e-mail normalizado em minúsculas
- ✅ Senha guardada como hash bcrypt, nunca em texto puro
- ✅ A resposta da API nunca devolve a senha nem o hash
- ✅ Validações do cadastro: e-mail repetido (409), senha curta e e-mail inválido (422)
- ✅ Geração de token JWT assinado, com tempo de expiração configurável
- ✅ Login (`POST /login`) com conferência da senha e devolução de token JWT
- ✅ Bloqueio de contas desativadas no login (retorna 403, só depois de a senha ser conferida)
- ✅ Rota protegida `GET /users/me`: devolve os dados do usuário logado, só com token válido

**Geral**
- ✅ Documentação interativa automática (Swagger UI)
- ✅ Persistência real em PostgreSQL
- ✅ Configurações sensíveis (chave secreta) lidas de arquivo `.env`, fora do código

## 🏗️ Como rodar o projeto localmente

### Pré-requisitos

- [Python 3.12+](https://www.python.org/)
- [Docker](https://www.docker.com/)
- [Poetry](https://python-poetry.org/)

### Passo a passo

1. Clone o repositório:
```bash
git clone https://github.com/wander671/ecommerce-api.git
cd ecommerce-api
```

2. Instale as dependências:
```bash
poetry install
```

3. Crie o arquivo `.env` na raiz do projeto (ele não vai para o GitHub, porque guarda segredos):
```
SECRET_KEY=cole_aqui_uma_chave_aleatoria
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
Para gerar uma chave aleatória:
```bash
poetry run python -c "import secrets; print(secrets.token_hex(32))"
```

4. Suba o banco de dados PostgreSQL:
```bash
docker compose up -d
```

5. Rode a aplicação:
```bash
poetry run python run.py
```

6. Acesse a documentação interativa em `http://localhost:8000/docs`

## 📚 Endpoints disponíveis

| Método | Rota                | Descrição                             |
|--------|---------------------|---------------------------------------|
| GET    | `/health`           | Verifica se a API está no ar          |
| GET    | `/products`         | Lista todos os produtos               |
| GET    | `/products/{id}`    | Busca um produto por ID               |
| POST   | `/products`         | Cria um novo produto                  |
| PUT    | `/products/{id}`    | Atualiza um produto                   |
| DELETE | `/products/{id}`    | Remove um produto                     |
| GET    | `/categories`       | Lista todas as categorias             |
| GET    | `/categories/{id}`  | Busca uma categoria por ID            |
| POST   | `/categories`       | Cria uma nova categoria               |
| PUT    | `/categories/{id}`  | Atualiza uma categoria                |
| DELETE | `/categories/{id}`  | Remove uma categoria                  |
| POST   | `/users`            | Cadastra um novo usuário              |
| POST   | `/login`            | Faz login e devolve um token          |
| GET    | `/users/me`         | Dados do usuário logado (exige token) |

## 🗺️ Roadmap de evolução

Este projeto está sendo construído em níveis progressivos de complexidade, como forma de estudo aprofundado de arquitetura de software.

- [x] **Nível Estágio** — CRUD básico com dados em memória
- [x] **Nível Júnior** — Persistência real com PostgreSQL + SQLAlchemy
- [ ] **Nível Pleno** — Em andamento 🚧
  - [x] Relacionamento entre tabelas (Produtos ↔ Categorias)
  - [x] CRUD completo de categorias, com bloqueio de exclusão
  - [x] Cadastro de usuários com hash de senha
  - [x] Login e autenticação JWT
    - [x] Configuração segura da chave secreta via `.env`
    - [x] Geração do token
    - [x] Schemas de login e de resposta do token
    - [x] Rota de login: busca do usuário, conferência da senha e devolução do token
    - [x] Bloqueio de usuários inativos no login
    - [x] Leitura e conferência do token (assinatura e validade)
    - [x] Função que descobre o usuário logado a partir do token
  - [ ] Proteção de rotas
    - [x] Primeira rota protegida (`GET /users/me`)
    - [ ] Proteger as rotas de escrita (produtos e categorias)
  - [ ] Carrinho e pedidos
  - [ ] Testes automatizados
- [ ] **Nível Sênior** — Arquitetura em camadas (Clean Architecture), operações assíncronas, filas de mensagens, cache, observabilidade, migrations com Alembic
- 💡 **Ideias futuras**
  - Chatbot de atendimento com IA
    - Rota `POST /chat`, com a chamada ao modelo feita no backend
    - Chave de API guardada no `.env`
    - Ferramentas de leitura: busca de produtos, estoque e status do pedido do próprio cliente
    - Depende de: login (JWT), carrinho e pedidos
    - Limite de mensagens por usuário, para controlar custo

## 🧠 Aprendizados até aqui

- Configuração de ambiente com Poetry
- Diferença entre drivers síncronos (`psycopg2`/`psycopg`) e assíncronos para PostgreSQL
- Containerização de banco de dados com Docker Compose
- Modelagem de dados com SQLAlchemy (models) e validação com Pydantic (schemas)
- Debugging de problemas reais de ambiente (conflito de portas, autenticação de banco)
- Relacionamentos entre tabelas no SQLAlchemy (`ForeignKey` e `relationship`)
- Limitação do `Base.metadata.create_all()`: ele cria tabelas novas, mas não altera tabelas existentes — motivo pelo qual ferramentas de migration (como Alembic) são necessárias em projetos reais
- Schemas Pydantic de entrada descartam em silêncio campos não declarados: se `category_id` não está no schema, o valor enviado simplesmente some, sem erro
- Duas funções com a mesma rota no FastAPI não geram erro: a primeira declarada responde e a outra nunca é chamada
- Regras de negócio na API (409 com mensagem clara) complementam as restrições do banco (`unique=True`), que sozinhas só geram erro 500 genérico
- O `create_all()` não corrige tabelas já criadas: se uma tabela nasce com estrutura incompleta, é preciso recriá-la
- Senhas são guardadas com hash bcrypt e salt, e o `response_model` do FastAPI impede que o hash apareça nas respostas
- Segredos (como a chave de assinatura de tokens) ficam em `.env`, protegido pelo `.gitignore`, e nunca no código
- Estrutura de um hash bcrypt: versão, custo, salt e hash. O salt fica dentro do próprio hash
- Um token JWT tem conteúdo legível. A segurança vem da assinatura, que impede alterações
- O conteúdo de um JWT usa campos padrão: `sub` (de quem é o token) e `exp` (quando expira)
- Datas com fuso explícito (`timezone.utc`) evitam bugs de horário local versus universal
- No login, a senha não tem tamanho mínimo no schema: a regra de senha forte vale no cadastro, e no login a API só confere se a senha bate, sem revelar as regras do sistema
- "Bearer" significa "portador": quem porta o token é aceito, e ele viaja no cabeçalho `Authorization`
- O login responde com a mesma mensagem para e-mail inexistente e para senha errada, para a API não revelar quais e-mails estão cadastrados
- Login usa `POST`, para os dados não irem na URL e ficarem registrados em históricos e logs
- Em Python, dar a uma variável o mesmo nome de uma função que será chamada na mesma função causa `UnboundLocalError`: o Python trata o nome como variável local desde a primeira linha
- 401 significa "não consegui confirmar quem você é" e 403 significa "sei quem você é, mas você não tem permissão"
- No login, a checagem de conta ativa vem depois da senha: assim, quem não sabe a senha não descobre quais contas existem ou estão desativadas
- Ao ler um token, a lista de algoritmos aceitos é fixada no servidor, para quem envia o token não poder escolher como ele é conferido
- Mesmo com token válido, o usuário é buscado no banco a cada requisição: assim uma conta apagada ou desativada deixa de entrar antes de o token expirar
- Token inválido, vencido ou adulterado recebem a mesma resposta (401), sem detalhar o motivo
- Com `Depends(get_current_user)`, o FastAPI executa a conferência do token antes da rota: se ela falhar, a rota nem chega a rodar

## 👤 Autor

Desenvolvido por [wander671](https://github.com/wander671) como projeto de estudo e portfólio.