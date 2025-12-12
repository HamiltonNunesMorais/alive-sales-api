from sqlalchemy.orm import Session
from fastapi import HTTPException
from app import schemas
from app.models import Client

# Criar cliente
def create_client(db: Session, client: schemas.ClientCreate):
    existing_client = db.query(Client).filter(Client.cnpj == client.cnpj).first()
    if existing_client:
        raise HTTPException(status_code=400, detail="Client with this CNPJ already exists")

    new_client = Client(
        name=client.name,
        cnpj=client.cnpj,
        email=client.email,
        phone=client.phone,
        address=client.address
    )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client

# Listar clientes
def get_all_clients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Client).offset(skip).limit(limit).all()

# Buscar cliente por ID
def get_client_by_id(db: Session, client_id: int):
    client = db.query(Client).filter(Client.id_client == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

# Buscar cliente por CNPJ
def get_client_by_cnpj(db: Session, cnpj: str):
    client = db.query(Client).filter(Client.cnpj == cnpj).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

# Atualizar cliente
def update_client(db: Session, client_id: int, client_update: schemas.ClientCreate):
    client = db.query(Client).filter(Client.id_client == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    client.name = client_update.name
    client.cnpj = client_update.cnpj
    client.email = client_update.email
    client.phone = client_update.phone
    client.address = client_update.address

    db.commit()
    db.refresh(client)
    return client

# Deletar cliente
def delete_client(db: Session, client_id: int):
    client = db.query(Client).filter(Client.id_client == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    db.delete(client)
    db.commit()
    return {"detail": "Client deleted successfully"}
