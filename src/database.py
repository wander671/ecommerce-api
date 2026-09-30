from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base

# Em vez de montar a URL como uma string única (que pode ter
# problemas de parsing com certos caracteres), usamos a classe
# URL.create do SQLAlchemy, que monta a conexão de forma segura,
# campo por campo.
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username="ecommerce_user",
    password="ecommerce_pass",
    host="localhost",
    port=5433,
    database="ecommerce_db",
)

# Engine: o objeto que gerencia a conexão com o banco.
# Não precisa mais do check_same_thread (isso era exclusivo do SQLite).
engine = create_engine(DATABASE_URL)

# Fábrica de sessões. Cada requisição da API vai abrir uma sessão,
# usar, e fechar.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base de todos os modelos (tabelas).
Base = declarative_base()

def get_db():
    """
    Dependency do FastAPI: entrega uma sessão pronta para cada
    requisição e garante que ela seja fechada no final, mesmo
    que aconteça um erro (por isso o try/finally com yield).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()