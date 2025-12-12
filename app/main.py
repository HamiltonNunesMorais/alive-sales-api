from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import timedelta, datetime

from app.database import Base, engine
from app.routers import clients_router, products_router, sales_router
from app.auth import SECRET_KEY, ALGORITHM  # importa constantes do auth

# Cria as tabelas no banco (se não existirem)
Base.metadata.create_all(bind=engine)

# Inicializa a aplicação FastAPI
app = FastAPI(
    title="ALIVE Sales API",
    description="API para gerenciamento de clientes, produtos e vendas",
    version="1.0.0"
)

# Middleware de CORS (se tiver front-end)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ajuste para domínios específicos em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui os routers
app.include_router(clients_router.router)
app.include_router(products_router.router)
app.include_router(sales_router.router)

# Endpoint raiz
@app.get("/")
def root():
    return {"message": "Welcome to ALIVE Sales API"}

# Healthcheck
@app.get("/health")
def health():
    return {"status": "ok"}

# Endpoint de login (gera token JWT)
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Exemplo simples: se username == "admin", role=admin; senão role=user
    role = "admin" if form_data.username == "admin" else "user"
    token_data = {
        "sub": form_data.username,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}
