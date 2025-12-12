from sqlalchemy.orm import Session
from fastapi import HTTPException
from app import schemas
from app.models import Product

# Criar produto
def create_product(db: Session, product: schemas.ProductCreate):
    existing_product = db.query(Product).filter(Product.plan_name == product.plan_name).first()
    if existing_product:
        raise HTTPException(status_code=400, detail="Product with this plan name already exists")

    new_product = Product(
        plan_name=product.plan_name,
        description=product.description,
        price=product.price
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

# Listar produtos
def get_all_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()

# Buscar produto por ID
def get_product_by_id(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id_product == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Atualizar produto
def update_product(db: Session, product_id: int, product_update: schemas.ProductCreate):
    product = db.query(Product).filter(Product.id_product == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.plan_name = product_update.plan_name
    product.description = product_update.description
    product.price = product_update.price

    db.commit()
    db.refresh(product)
    return product

# Deletar produto
def delete_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id_product == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"detail": "Product deleted successfully"}
