from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr


# CONFIGURACIÓN JWT


SECRET_KEY = "clave_super_secreta_2026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Endpoint donde se obtiene el token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



# MODELOS


class User(BaseModel):
    username: str
    email: EmailStr


class UserInDB(User):
    password: str


class TokenData(BaseModel):
    username: Optional[str] = None



# USUARIOS SIMULADOS (BD FALSA)


fake_users_db = {
    "arturo": {
        "username": "arturo",
        "email": "arturo@email.com",
        "password": "1234"
    }
}


# FUNCIONES DE USUARIO


def verify_password(plain_password: str, stored_password: str):
    return plain_password == stored_password


def get_user(username: str):
    user = fake_users_db.get(username)
    if user:
        return UserInDB(**user)
    return None


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user



# CREACIÓN DEL TOKEN JWT


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt



# VALIDACIÓN DEL TOKEN


async def get_current_user(token: str = Depends(oauth2_scheme)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)

    except JWTError:
        raise credentials_exception

    user = get_user(username=token_data.username)

    if user is None:
        raise credentials_exception

    return user