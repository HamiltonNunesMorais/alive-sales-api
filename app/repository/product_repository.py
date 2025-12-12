from sqlalchemy.orm import Session
from app import models, schemas
import uuid

# ---------------------------
# CREATE
# ---------------------------
def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(
        id_product=str(uuid.uuid4()),
        plan_name=product.plan_name,
        description=product.description,
        price=product.price
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


# ---------------------------
# READ
# ---------------------------
def get_all_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()


def get_product_by_id(db: Session, product_id: str):
    return db.query(models.Product).filter(models.Product.id_product == product_id).first()


def get_product_by_name(db: Session, plan_name: str):
    return db.query(models.Product).filter(models.Product.plan_name == plan_name).first()
