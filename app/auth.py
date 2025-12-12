from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "segredo_local"
ALGORITHM = "HS256"

class TokenData(BaseModel):
    username: str | None = None
    role: str | None = None

# Função para verificar token
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return TokenData(username=username, role=role)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
