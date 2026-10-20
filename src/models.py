from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from src.database import Base

class CategoryModel(Base):
    """Representa a TABELA 'categories' no banco de dados."""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)

    # O relationship() não cria uma coluna no banco, mas permite
    # que, dado um objeto CategoryModel, eu possa acessar todos os
    # produtos que pertencem a essa categoria com category.products.
    products = relationship("ProductModel", back_populates="category")


class ProductModel(Base):
    """Representa a TABELA 'products' no banco de dados."""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    stock = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

    # A coluna category_id é uma chave estrangeira que referencia a tabela categories.
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    # O relationship() não cria uma coluna no banco, mas permite
    # que, dado um objeto ProductModel, eu possa acessar a categoria
    category = relationship("CategoryModel", back_populates="products")


class UserModel(Base):
    """Representa a TABELA 'users' no banco de dados."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)

    # unique=True: o banco recusa dois usuários com o mesmo e-mail.
    # index=True: cria um índice, que acelera a busca por e-mail
    # (e o login vai buscar por e-mail a cada tentativa).
    email = Column(String, nullable=False, unique=True, index=True)

    # Repare no nome: hashed_password, e não password. A senha
    # NUNCA é guardada como o usuário digitou. Guardamos só o
    # "hash", uma versão embaralhada que não dá para desfazer.
    # Se o banco vazar, as senhas reais não vazam junto.
    hashed_password = Column(String, nullable=False)

    # Permite desativar uma conta sem apagá-lá do banco. Usuário desativado não consegue logar.
    is_active = Column(Boolean, default=True, nullable=False)

    




