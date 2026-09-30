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

## 📋 Funcionalidades

- ✅ Listar produtos
- ✅ Buscar produto por ID
- ✅ Criar produto
- ✅ Atualizar produto (parcialmente)
- ✅ Deletar produto
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

3. Suba o banco de dados PostgreSQL:
```bash
docker compose up -d
```

4. Rode a aplicação:
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

## 🗺️ Roadmap de evolução

Este projeto está sendo construído em níveis progressivos de complexidade, como forma de estudo aprofundado de arquitetura de software.

- [x] **Nível Estágio** — CRUD básico com dados em memória
- [x] **Nível Júnior** — Persistência real com PostgreSQL + SQLAlchemy (você está aqui)
- [ ] **Nível Pleno** — Autenticação JWT, relacionamentos entre tabelas (usuários, pedidos, carrinho), testes automatizados
- [ ] **Nível Sênior** — Arquitetura em camadas (Clean Architecture), operações assíncronas, filas de mensagens, cache, observabilidade

## 🧠 Aprendizados deste nível

- Configuração de ambiente com Poetry
- Diferença entre drivers síncronos (`psycopg2`/`psycopg`) e assíncronos para PostgreSQL
- Containerização de banco de dados com Docker Compose
- Modelagem de dados com SQLAlchemy (models) e validação com Pydantic (schemas)
- Debugging de problemas reais de ambiente (conflito de portas, autenticação de banco)

## 👤 Autor

Desenvolvido por [wander671](https://github.com/wander671) como projeto de estudo e portfólio.