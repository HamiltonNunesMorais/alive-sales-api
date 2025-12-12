from pydantic import BaseModel, Field
from datetime import datetime

# -------------------------
# Client
# -------------------------
class ClientBase(BaseModel):
    name: str
    cnpj: str = Field(..., min_length=14, max_length=14, pattern=r"^\d{14}$")  # apenas 14 dígitos

class ClientCreate(ClientBase):
    email: str | None = None
    phone: str | None = None
    address: str | None = None

class Client(ClientBase):
    id_client: int
    email: str | None = None
    phone: str | None = None
    address: str | None = None

    class Config:
        from_attributes = True


# -------------------------
# Product
# -------------------------
class ProductBase(BaseModel):
    plan_name: str
    description: str | None = None
    price: float

class ProductCreate(ProductBase):
    plan_name: str
    description: str | None = None
    price: float

class Product(ProductBase):
    id_product: int

    class Config:
        from_attributes = True


# -------------------------
# Sale
# -------------------------
class SaleBase(BaseModel):
    cnpj: str = Field(..., min_length=14, max_length=14, pattern=r"^\d{14}$")
    plan_id: int
    quantity: int = Field(..., gt=0)
    installation_address: str

class SaleCreate(SaleBase):
    pass

class Sale(SaleBase):
    id_sale: int
    sale_date: datetime

    class Config:
        from_attributes = True
