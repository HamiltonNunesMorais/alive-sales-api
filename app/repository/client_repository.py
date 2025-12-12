from sqlalchemy.orm import Session
from app import models, schemas
import uuid

# ---------------------------
# CREATE
# ---------------------------
def create_client(db: Session, client: schemas.ClientCreate):
    db_client = models.Client(
        id_client=str(uuid.uuid4()),
        name=client.name,
        cnpj=client.cnpj,
        email=client.email,
        phone=client.phone,
        address=client.address
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


# ---------------------------
# READ
# ---------------------------
def get_all_clients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Client).offset(skip).limit(limit).all()


def get_client_by_id(db: Session, client_id: str):
    return db.query(models.Client).filter(models.Client.id_client == client_id).first()


def get_client_by_cnpj(db: Session, cnpj: str):
    return db.query(models.Client).filter(models.Client.cnpj == cnpj).first()
