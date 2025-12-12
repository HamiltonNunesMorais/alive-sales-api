from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ClientCreate, Client
from app.services import client_service

router = APIRouter(
    prefix="/api/v1/clients",
    tags=["clients"]
)

@router.post("/", response_model=Client)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    return client_service.create_client(db, client)

@router.get("/", response_model=list[Client])
def get_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return client_service.get_all_clients(db, skip, limit)

@router.get("/{client_id}", response_model=Client)
def get_client(client_id: int, db: Session = Depends(get_db)):
    return client_service.get_client_by_id(db, client_id)

@router.get("/cnpj/{cnpj}", response_model=Client)
def get_client_by_cnpj(cnpj: str, db: Session = Depends(get_db)):
    return client_service.get_client_by_cnpj(db, cnpj)

@router.put("/{client_id}", response_model=Client)
def update_client(client_id: int, client_update: ClientCreate, db: Session = Depends(get_db)):
    return client_service.update_client(db, client_id, client_update)

@router.delete("/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    return client_service.delete_client(db, client_id)
