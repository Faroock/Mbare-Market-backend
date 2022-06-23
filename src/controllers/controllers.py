from typing import List

from models.models import Rol, User, session
from models.models import Country, City, State

def get_all_countries() -> List[Country]:
    query = session.query(Country)
    return query.all()

def get_country_by_id(country_id: int) -> Country:
    query = session.query(Country).filter(Country.id == country_id)
    return query.first()

def get_country_by_name(country_name: str) ->Country:
    query = session.query(Country).filter(Country.country.ilike(f'%{country_name.lower()}%'))
    return query.first()

def get_country_by_code(country_code: str) -> Country:
    query = session.query(Country).filter(Country.code.ilike(f'{country_code.lower()}'))
    return query.first()

def get_states_by_country_id(country_id: int) -> List[State]:
    query = session.query(
            State.country_id,
            Country.country,
            Country.code.label('country_code'),
            State.id.label('state_id'),
            State.code.label('state_code'),
            State.state
        ).filter(State.country_id == country_id).join(Country, State.country_id == Country.id, isouter=True)
    return query.all()

def get_states_by_country_name(country_name: str) -> List[State]:
    query = session.query(
            State.country_id,
            Country.country,
            Country.code.label('country_code'),
            State.id.label('state_id'),
            State.code.label('state_code'),
            State.state
        ).join(Country, State.country_id == Country.id).filter(Country.country.ilike(f'%{country_name.lower()}%'))
    return query.all()

def get_states_by_country_code(country_code: str) -> List[State]:
    query = session.query(
        State.country_id,
        Country.country,
        Country.code.label('country_code'),
        State.id.label('state_id'),
        State.code.label('state_code'),
        State.state
    ).join(Country, State.country_id == Country.id).filter(Country.code.ilike(f'{country_code.lower()}'))
    return query.all()

def get_all_states() -> List[State]:
    query = session.query(
            State.country_id,
            Country.country,
            Country.code.label('country_code'),
            State.id.label('state_id'),
            State.code.label('state_code'),
            State.state
        ).join(Country, State.country_id == Country.id)
    return query.all()

def get_state_by_name(state_name: str, country_id: int) -> State:
    query = session.query(State).filter(State.country_id == country_id).filter(State.state.ilike(f'%{state_name.lower()}%'))
    return query.first()

def get_state_by_code(state_code: str, country_id: int) -> State:
    query = session.query(State).filter(State.country_id == country_id).filter(State.code.ilike(f'{state_code.lower()}'))
    return query.first()

def get_all_cities() -> List[City]:
    query = session.query(
        City.id_country.label('country_id'),
        Country.country,
        Country.code.label('country_code'),
        City.id.label('city_id'),
        City.city
    ).join(Country, City.id_country == Country.id)
    return query.all()

def get_cities_by_country_id(country_id: int) -> List[City]:
    query = session.query(
        City.id_country.label('country_id'),
        Country.country,
        Country.code.label('country_code'),
        City.id.label('city_id'),
        City.city
    ).join(Country, City.id_country == Country.id).filter(City.id_country == country_id)
    return query.all()

def get_cities_by_country_name(country_name: str) -> List[City]:
    query = session.query(
        City.id_country.label('country_id'),
        Country.country,
        Country.code.label('country_code'),
        City.id.label('city_id'),
        City.city
    ).join(Country, City.id_country == Country.id).filter(Country.country.ilike(f'%{country_name.lower()}%'))
    return query.all()

def get_cities_by_country_code(country_code: str) -> List[City]:
    query = session.query(
        City.id_country.label('country_id'),
        Country.country,
        Country.code.label('country_code'),
        City.id.label('city_id'),
        City.city
    ).join(Country, City.id_country == Country.id).filter(Country.code.ilike(f'{country_code.lower()}'))
    return query.all()

def get_user_by_email(email: str) -> User:
    query = session.query(
        User.vekn_id,
        User.nick_name,
        User.name,
        User.country.label('id_country'),
        Country.country,
        User.state.label('id_state'),
        State.state,
        User.city,
        User.email,
        User.password,
        User.rol.label('id_rol'),
        Rol.rol,
        Rol.permiso
    ).join(Rol, User.rol == Rol.id).join(Country, User.country == Country.id).join(State, User.state == State.id, isouter=True).filter(User.email.ilike(email.lower()))
    return query.first()