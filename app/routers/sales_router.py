from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import SaleCreate, Sale
from app.services import sale_service
from app.auth import get_current_user, TokenData

router = APIRouter(
    prefix="/api/v1/sales",
    tags=["sales"]
)

@router.post("/", response_model=Sale)
def create_sale(sale: SaleCreate, db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):
    # Usuário comum e admin podem criar
    return sale_service.create_sale(db, sale)

@router.get("/", response_model=list[Sale])
def get_sales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):
    # Usuário comum e admin podem listar
    return sale_service.get_all_sales(db, skip, limit)

@router.get("/{sale_id}", response_model=Sale)
def get_sale(sale_id: int, db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):
    return sale_service.get_sale_by_id(db, sale_id)

@router.put("/{sale_id}", response_model=Sale)
def update_sale(sale_id: int, sale_update: SaleCreate, db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return sale_service.update_sale(db, sale_id, sale_update)

@router.delete("/{sale_id}")
def delete_sale(sale_id: int, db: Session = Depends(get_db), user: TokenData = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return sale_service.delete_sale(db, sale_id)
