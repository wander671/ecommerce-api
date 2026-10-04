from sqlalchemy import Column, Integer, String, Float, ForeignKey
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

    # A coluna category_id é uma chave estrangeira que referencia a tabela categories.
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    # O relationship() não cria uma coluna no banco, mas permite
    # que, dado um objeto ProductModel, eu possa acessar a categoria
    category = relationship("CategoryModel", back_populates="products")

