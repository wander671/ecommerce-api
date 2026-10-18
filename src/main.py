from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session
from typing import Optional

from src.database import Base, engine, get_db
from src.models import ProductModel, CategoryModel

# Cria as tabelas no banco se elas ainda não existirem.
# Ele olha todas as classes que herdam de Base (ProductModel)
# e cria a tabela correspondente. Roda uma vez ao iniciar o app.
# Mais pra frente vamos trocar isso por migrations (Alembic).
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-commerce API",
    description="CRUD simples de produtos, dados em memória",
    version="0.1.0",
)

# ==========================================
# SCHEMAS (Pydantic): formato dos dados na API
# ==========================================

class Product(BaseModel):
    """Formato do produto na RESPOSTA da API."""

    # from_attributes=True permite ao Pydantic ler dados de um
    # objeto SQLAlchemy (ProductModel), e não só de dicionários.
    # Sem isso, retornar um ProductModel daria erro.
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    price: float
    description: Optional[str] = None  # Optional = pode não vir, então tem valor padrão None
    stock: int = 0  # valor padrão 0 se não for informado
    category_id: Optional[int] = None # categoria pode ser nula (sem categoria)

class Category(BaseModel):
    """Formato da categoria na resposta da API."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str] = None

class CategoryCreate(BaseModel):
    """Dados que o cliente envia para CRIAR uma categoria (sem id)."""
    name: str
    description: Optional[str] = None

class CategoryUpdate(BaseModel):
    """Dados para ATUALIZAR uma categoria: todos opcionais."""
    name: Optional[str] = None
    description: Optional[str] = None

class ProductCreate(BaseModel):
    """Dados que o cliente envia para CRIAR um produto (sem id)."""
    name: str
    price: float
    description: Optional[str] = None
    stock: int = 0
    category_id: Optional[int] = None

class ProductUpdate(BaseModel):
    """Dados para ATUALIZAR: todos opcionais."""
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    stock: Optional[int] = None
    category_id: Optional[int] = None

# ==========================================
# ENDPOINTS
# ==========================================
# Repare: agora são "def" e não "async def". Como o SQLAlchemy que
# estamos usando é SÍNCRONO, ele bloquearia o servidor dentro de uma
# função async. Com "def" normal, o FastAPI roda a função numa thread
# separada e o servidor continua atendendo outras requisições.
# Só voltamos ao "async def" quando migrarmos para SQLAlchemy async.

@app.get("/health")
async def health_check():
    """Endpoint simples pra confirmar que a API está no ar."""
    return {"status": "ok"}


@app.get("/products", response_model=list[Product])
async def list_products(db: Session = Depends(get_db)):
    """
    LISTAR produtos.

    db: Session = Depends(get_db) é a injeção de dependência: o
    FastAPI chama get_db(), recebe uma sessão aberta e a entrega
    como argumento 'db'. Ao fim da requisição, fecha a sessão.
    """
    # db.query(ProductModel) monta um "SELECT * FROM products".
    # .all() executa e devolve uma lista de objetos ProductModel
    return db.query(ProductModel).all()


@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """BUSCAR um produto por ID."""
    # .filter(...) equivale ao WHERE do SQL.
    # .first() devolve o primeiro resultado, ou None se não achar.
    product = db.query(ProductModel). filter(ProductModel.id == product_id).first()

    if product is None:
        # HTTPException é como você retorna erros HTTP no FastAPI.
        # status_code 404 = "não encontrado".
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    return product


@app.post("/products", response_model=Product, status_code=201)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    """CRIAR um produto."""
    # Se o cliente informou uma categoria, ela precisa existir.
    if product_data.category_id is not None:
        category = db.query(CategoryModel).filter(
            CategoryModel.id == product_data.category_id
        ).first()
        if category is None:
            raise HTTPException(status_code=400, detail="Categoria não existe")

    new_product = ProductModel(**product_data.model_dump())

    db.add(new_product)         # marca para inserir (ainda não foi ao banco)
    db.commit()                  # confirma a transação: INSERT acontece aqui
    db.refresh(new_product)     # recarrega o objeto do banco para pegar o id gerado

    return new_product


@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):

    """ATUALIZAR um produto (parcialmente)."""
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    # exclude_unset=True: só os campos que o cliente realmente enviou.
    update_data = product_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(product, key, value) # equivale a product.key = value, de forma dinâmica

    db.commit()
    db.refresh(product)

    return product


@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """DELETAR um produto."""
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    db.delete(product)
    db.commit()


@app.get("/categories", response_model=list[Category])
def list_categories(db: Session = Depends(get_db)):
    """LISTAR categorias."""
    return db.query(CategoryModel).all()


@app.get("/categories/{category_id}", response_model=Category)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """BUSCAR uma categoria por ID."""
    category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    
    if category is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    return category

@app.put("/categories/{category_id}", response_model=Category)
def update_category(
    category_id: int, category_data: CategoryUpdate, db: Session = Depends(get_db)
):
    """ATUALIZAR uma categoria (parcialmente)."""
    category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()

    if category is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    update_data = category_data.model_dump(exclude_unset=True)

    new_name = update_data.get("name")
    if new_name is not None:
        duplicate = db.query(CategoryModel).filter(
            CategoryModel.name == new_name,
            CategoryModel.id != category_id,
        ).first()
        if duplicate:
            raise HTTPException(
                status_code=409,
                detail="Já existe uma categoria com esse nome",
            )

    for key, value in update_data.items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)

    return category



@app.post("/categories", response_model=Category, status_code=201)
def create_category(category_data: CategoryCreate, db: Session = Depends(get_db)):
    """CRIAR uma categoria."""
    new_category = CategoryModel(**category_data.model_dump())

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category

@app.delete("/categories/{category_id}", status_code=204)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Deletar uma categoria. Só é permitido se não houver produtos associados."""
    category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    # Verificar se há produtos associados
    products = db.query(ProductModel).filter(ProductModel.category_id == category_id).all()
    if products:
        raise HTTPException(status_code=409, detail="Não é possível excluir uma categoria que possui produtos associados")

    db.delete(category)
    db.commit()