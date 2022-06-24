import os
from controllers.controllers import get_country_by_code, get_country_by_name, get_state_by_code, get_state_by_name, get_user_by_email

from models.models import NewUser, TokenData, db
from models.models import User

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends, status
from jose import jwt, JWTError
from dotenv import load_dotenv

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def create_user_db(new_user: NewUser) -> User:
    country = get_country_by_name(new_user.country)
    if not country:
        country = get_country_by_code(new_user.country)
    country_id = country.id if country else new_user.country
    state = get_state_by_name(new_user.state, country_id)
    if not state:
        state = get_state_by_code(new_user.state, country_id)
    state_id = state.id if state else new_user.state
    usuario = User(
        vekn_id = new_user.vekn_id,
        nick_name = new_user.nick_name,
        name = new_user.name,
        country = country_id,
        state = state_id,
        city = new_user.city,
        email = new_user.email,
        password = hash_password(new_user.password),
        llave = new_user.email
    )
    return {'user': usuario, 'return': db.grabar_modelo(usuario)}

def change_password_user(email: str, new_password: str) -> User:
    user = get_user_by_email(email)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Usuario no existe')
    usuario = User(
        vekn_id = user.vekn_id,
        nick_name = user.nick_name,
        name = user.name,
        country = user.id_country,
        state = user.id_state,
        city = user.city,
        email = user.email,
        password = hash_password(new_password),
        llave = user.email,
        rol = user.id_rol
    )
    db.grabar_modelo(usuario)
    return {'user': usuario, 'return': db.grabar_modelo(usuario)}

def authenticate_user(username: str, password: str):
    user = get_user_by_email(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        rol: str = payload.get('rol')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, rol=rol)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(token_data.username)
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)