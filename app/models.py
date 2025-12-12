from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base

class Client(Base):
    __tablename__ = "clients"
    id_client = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    cnpj = Column(String(14), unique=True, nullable=False)  # 14 dígitos sem formatação
    email = Column(String(100))
    phone = Column(String(20))
    address = Column(String(200))

    sales = relationship("Sale", back_populates="client")


class Product(Base):
    __tablename__ = "products"
    id_product = Column(Integer, primary_key=True, autoincrement=True)
    plan_name = Column(String(50), nullable=False)
    description = Column(String(200))
    price = Column(Float, nullable=False)

    sales = relationship("Sale", back_populates="product")


class Sale(Base):
    __tablename__ = "sales"
    id_sale = Column(Integer, primary_key=True, autoincrement=True)
    id_client = Column(Integer, ForeignKey("clients.id_client"), nullable=False)
    id_product = Column(Integer, ForeignKey("products.id_product"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    installation_address = Column(String(200), nullable=False)
    sale_date = Column(DateTime(timezone=True), server_default=func.now())

    client = relationship("Client", back_populates="sales")
    product = relationship("Product", back_populates="sales")
