from sqlalchemy.orm import Session
from app import models, schemas
import uuid
from datetime import datetime

# ---------------------------
# CREATE
# ---------------------------
def create_sale(db: Session, sale: schemas.SaleCreate):
    db_sale = models.Sale(
        id_sale=str(uuid.uuid4()),
        id_client=sale.id_client,
        id_product=sale.id_product,
        quantity=sale.quantity,
        sale_date=datetime.utcnow()
    )
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale


# ---------------------------
# READ
# ---------------------------
def get_all_sales(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Sale).offset(skip).limit(limit).all()


def get_sale_by_id(db: Session, sale_id: str):
    return db.query(models.Sale).filter(models.Sale.id_sale == sale_id).first()
