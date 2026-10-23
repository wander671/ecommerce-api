# 🛒 E-commerce API

API REST para um sistema de e-commerce, construída como projeto de estudo com evolução progressiva de arquitetura — do nível júnior ao sênior.

## 📌 Status atual: Nível Júnior

CRUD completo de produtos com persistência real em banco de dados relacional.

## 🚀 Tecnologias

- **[FastAPI](https://fastapi.tiangolo.com/)** — framework web assíncrono em Python
- **[SQLAlchemy](https://www.sqlalchemy.org/)** — ORM para comunicação com o banco de dados
- **[PostgreSQL](https://www.postgresql.org/)** — banco de dados relacional
- **[Docker](https://www.docker.com/)** — containerização do banco de dados
- **[Poetry](https://python-poetry.org/)** — gerenciamento de dependências
- **[bcrypt](https://pypi.org/project/bcrypt/)** — hash seguro de senhas

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

**Usuários**
- ✅ Cadastro de usuário (`POST /users`), com e-mail normalizado em minúsculas
- ✅ Senha guardada como hash bcrypt, nunca em texto puro
- ✅ A resposta da API nunca devolve a senha nem o hash
- ✅ Validações do cadastro: e-mail repetido (409), senha curta e e-mail inválido (422)
- ✅ Configurações sensíveis (chave secreta) lidas de arquivo `.env`, fora do código
- ✅ Geração de token JWT assinado, com tempo de expiração configurável
- 🔄 Login e autenticação com token JWT (em desenvolvimento)

**Geral**
- ✅ Documentação interativa automática (Swagger UI)
- ✅ Persistência real em PostgreSQL

## 🏗️ Como rodar o projeto localmente

### Pré-requisitos

- [Python 3.12+](https://www.python.org/)
- [Docker](https://www.docker.com/)
- [Poetry](https://python-poetry.org/)

### Passo a passo

1. Clone o repositório:
```bash
git clone https://github.com/SEU_USUARIO/ecommerce.git
cd ecommerce
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

5. Acesse a documentação interativa:
http://localhost:8000/docs


## 📚 Endpoints disponíveis

| Método | Rota                  | Descrição                     |
|--------|------------------------|--------------------------------|
| GET    | `/health`              | Verifica se a API está no ar  |
| GET    | `/products`            | Lista todos os produtos       |
| GET    | `/products/{id}`       | Busca um produto por ID       |
| POST   | `/products`            | Cria um novo produto          |
| PUT    | `/products/{id}`       | Atualiza um produto           |
| DELETE | `/products/{id}`       | Remove um produto             |
| GET    | `/categories`          | Lista todas as categorias     |
| GET    | `/categories/{id}`     | Busca uma categoria por ID    |
| POST   | `/categories`          | Cria uma nova categoria       |
| DELETE | `/categories/{id}`     | Remove uma categoria          |
| PUT    | `/categories/{id}`     | Atualiza uma categoria        |
| POST   | `/users`               | Cadastra um novo usuário      |

## 🗺️ Roadmap de evolução

Este projeto está sendo construído em níveis progressivos de complexidade, como forma de estudo aprofundado de arquitetura de software.

- [x] **Nível Estágio** — CRUD básico com dados em memória
- [x] **Nível Júnior** — Persistência real com PostgreSQL + SQLAlchemy
- [ ] **Nível Pleno** — Em andamento 🚧
    - [x] Relacionamento entre tabelas (Produtos ↔ Categorias)
  - [x] CRUD completo de categorias, com bloqueio de exclusão
  - [x] Cadastro de usuários com hash de senha
  - [x] Configuração segura da chave secreta via `.env`
  - [ ] Login e autenticação JWT
  - [x] Geração do token
  - [ ] Rota de login
  - [ ] Proteção de rotas
  - [ ] Carrinho e pedidos
  - [ ] Testes automatizados
- [ ] **Nível Sênior** — Arquitetura em camadas (Clean Architecture), operações assíncronas, filas de mensagens, cache, observabilidade, migrations com Alembic

## 🧠 Aprendizados deste nível

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

## 👤 Autor

Desenvolvido por [wander671](https://github.com/wander671) como projeto de estudo e portfólio.