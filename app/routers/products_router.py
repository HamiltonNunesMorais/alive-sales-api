from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ProductCreate, Product
from app.services import product_service

router = APIRouter(
    prefix="/api/v1/products",
    tags=["products"]
)

@router.post("/", response_model=Product)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return product_service.create_product(db, product)

@router.get("/", response_model=list[Product])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return product_service.get_all_products(db, skip, limit)

@router.get("/{product_id}", response_model=Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return product_service.get_product_by_id(db, product_id)

@router.put("/{product_id}", response_model=Product)
def update_product(product_id: int, product_update: ProductCreate, db: Session = Depends(get_db)):
    return product_service.update_product(db, product_id, product_update)

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    return product_service.delete_product(db, product_id)
