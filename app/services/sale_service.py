from sqlalchemy.orm import Session
from fastapi import HTTPException
from app import schemas
from app.models import Client, Product, Sale

# Criar venda
def create_sale(db: Session, sale: schemas.SaleCreate):
    client = db.query(Client).filter(Client.cnpj == sale.cnpj).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    product = db.query(Product).filter(Product.id_product == sale.plan_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if sale.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than zero")

    new_sale = Sale(
        id_client=client.id_client,
        id_product=product.id_product,
        quantity=sale.quantity,
        installation_address=sale.installation_address
    )
    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)

    return schemas.Sale(
        id_sale=new_sale.id_sale,
        cnpj=client.cnpj,
        plan_id=product.id_product,
        quantity=new_sale.quantity,
        installation_address=new_sale.installation_address,
        sale_date=new_sale.sale_date
    )

# Listar vendas
def get_all_sales(db: Session, skip: int = 0, limit: int = 100):
    sales = db.query(Sale).offset(skip).limit(limit).all()
    result = []
    for s in sales:
        client = db.query(Client).filter(Client.id_client == s.id_client).first()
        product = db.query(Product).filter(Product.id_product == s.id_product).first()
        result.append(
            schemas.Sale(
                id_sale=s.id_sale,
                cnpj=client.cnpj if client else None,
                plan_id=product.id_product if product else None,
                quantity=s.quantity,
                installation_address=s.installation_address,
                sale_date=s.sale_date
            )
        )
    return result

# Buscar venda por ID
def get_sale_by_id(db: Session, sale_id: int):
    s = db.query(Sale).filter(Sale.id_sale == sale_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Sale not found")

    client = db.query(Client).filter(Client.id_client == s.id_client).first()
    product = db.query(Product).filter(Product.id_product == s.id_product).first()

    return schemas.Sale(
        id_sale=s.id_sale,
        cnpj=client.cnpj if client else None,
        plan_id=product.id_product if product else None,
        quantity=s.quantity,
        installation_address=s.installation_address,
        sale_date=s.sale_date
    )

# Atualizar venda
def update_sale(db: Session, sale_id: int, sale_update: schemas.SaleCreate):
    s = db.query(Sale).filter(Sale.id_sale == sale_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Sale not found")

    client = db.query(Client).filter(Client.cnpj == sale_update.cnpj).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    product = db.query(Product).filter(Product.id_product == sale_update.plan_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    s.id_client = client.id_client
    s.id_product = product.id_product
    s.quantity = sale_update.quantity
    s.installation_address = sale_update.installation_address

    db.commit()
    db.refresh(s)

    return schemas.Sale(
        id_sale=s.id_sale,
        cnpj=client.cnpj,
        plan_id=product.id_product,
        quantity=s.quantity,
        installation_address=s.installation_address,
        sale_date=s.sale_date
    )

# Deletar venda
def delete_sale(db: Session, sale_id: int):
    s = db.query(Sale).filter(Sale.id_sale == sale_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Sale not found")

    db.delete(s)
    db.commit()
    return {"detail": "Sale deleted successfully"}
