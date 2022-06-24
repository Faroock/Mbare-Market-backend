import os

import uvicorn

from fastapi import FastAPI
from fastapi import Query, Body, Form, Path
from fastapi import HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware

from typing import Optional
from dotenv import load_dotenv
from controllers.cartas import todas_las_cartas

from controllers.controllers import get_all_cities, get_all_countries, get_all_states, get_cities_by_country_code, get_cities_by_country_id, get_cities_by_country_name, get_states_by_country_code, get_states_by_country_id, get_states_by_country_name
from controllers.secutity import authenticate_user, change_password_user, create_access_token, create_user_db, get_current_active_user, hash_password
from controllers.vekn import get_usuario_from_vekn
from models.models import NewUser, User

app = FastAPI()

load_dotenv()
origins = os.getenv('CORS').split(',')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def home():
    return {"message": "OK"}

@app.get('/all_cards', tags=['Cartas'])
def get_all_cards(type: Optional[str] = Query(default='Library'), page: Optional[int] = Query(default=1), page_size: Optional[int] = Query(default=15)):
    all_cards = todas_las_cartas(type, page, page_size)
    return all_cards

@app.get('/countries', tags=['Demográficos'])
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

@app.get('/cities', tags=['Demográficos'])
def get_city(country_id: Optional[int] = Query(None), country_name: Optional[str] = Query(None), country_code: Optional[str] = Query(None)):
    if (country_id):
        return get_cities_by_country_id(country_id)
    if (country_name):
        return get_cities_by_country_name(country_name)
    if (country_code):
        return get_cities_by_country_code(country_code)
    return get_all_cities()

@app.get('/usuario/{vekn_id}', tags=['Usuario'])
def get_user_from_vekn(vekn_id: int = Path(...)):
    return get_usuario_from_vekn(vekn_id)

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

@app.put('/user/create', tags=['Usuario'])
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