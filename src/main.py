import os

import uvicorn

from fastapi import FastAPI
from fastapi import Query, Body, Form
from fastapi import HTTPException, status, Depends
from fastapi.responses import JSONResponse

from typing import Optional
from datetime import timedelta
from dotenv import load_dotenv

from controllers.controllers import get_all_cities, get_all_countries, get_all_states, get_cities_by_country_code, get_cities_by_country_id, get_cities_by_country_name, get_states_by_country_code, get_states_by_country_id, get_states_by_country_name
from controllers.secutity import authenticate_user, change_password_user, create_access_token, create_user_db, get_current_active_user, hash_password
from models.models import NewUser, User, UserInput

app = FastAPI()

load_dotenv()

@app.get(f'/countries', tags=['Demográficos'])
def get_countries():
    return get_all_countries()

@app.get(f'/states', tags=['Demográficos'])
def get_estados_pais(country_id: Optional[int] = Query(None), country_name: Optional[str] = Query(None), country_code: Optional[str] = Query(None)):
    if (country_id):
        return get_states_by_country_id(country_id)
    if (country_name):
        return get_states_by_country_name(country_name)
    if (country_code):
        return get_states_by_country_code(country_code)
    return get_all_states()

@app.get(f'/cities', tags=['Demográficos'])
def get_city(country_id: Optional[int] = Query(None), country_name: Optional[str] = Query(None), country_code: Optional[str] = Query(None)):
    if (country_id):
        return get_cities_by_country_id(country_id)
    if (country_name):
        return get_cities_by_country_name(country_name)
    if (country_code):
        return get_cities_by_country_code(country_code)
    return get_all_cities()

@app.post(f'/login', tags=['Usuario'])
@app.post('/token', tags=['Usuario'])
def login(username: str = Form(...), password: str = Form(...)):
   
    if (not username) or (not password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Se necesita de un usuario y un password para loguearse')
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = create_access_token({"sub": user.email, "rol": user.permiso})
    return {"access_token": access_token, "token_type": "bearer"}

@app.put(f'/user/create', tags=['Usuario'])
def create_user(new_user: NewUser = Body(...)):
    usuario = create_user_db(new_user)
    return usuario

@app.post('/user/password', tags=['Usuario'])
def change_password(
    new_password: str,
    username: Optional[str] = None,
    current_user: User = Depends(get_current_active_user)
):
    if username:
        if current_user.permiso == 'root':
            user = change_password_user(username, new_password)
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'El usuario conectado {current_user.email} no está autorizado para cambiarle la contraseña al usuario {username}')
    else:
        user = change_password_user(current_user.email, new_password)
    return user

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PUERTO_BACKEND")), debug=True, reload=True)