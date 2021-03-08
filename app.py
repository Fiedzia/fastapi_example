from logging import getLogger

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

import sqlalchemy

from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
logger = getLogger(__name__)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def as_dict(obj):
    return {c.name: str(getattr(obj, c.name)) for c in obj.__table__.columns}


class User(BaseModel):
    name: str


class Account(BaseModel):
    name: str


class Address(BaseModel):
    name: str
    content: str


@app.get("/")
def show_users_accounts_and_addresses(db: Session = Depends(get_db)):
    users = list(map(
        as_dict,
        db.query(models.User)
            .filter()
            .order_by(models.User.id)
            .all()
    ))
    accounts = list(map(
        as_dict,
        db.query(models.Account)
            .filter()
            .order_by(models.Account.id)
            .all()
    ))
    addresses = list(map(
        as_dict,
        db.query(models.Address)
            .filter()
            .order_by(models.Address.id)
            .all()
    ))
    user_address_mappings = list(map(
        as_dict,
        db.query(models.UserAddressMapping)
            .filter()
            .order_by(models.UserAddressMapping.id)
            .all()
    ))
    return {
        'users': users,
        'accounts': accounts,
        'addresses': addresses,
        'user_address_mappings': user_address_mappings
    }


@app.post("/user/")
def create_user(*, user: User, db: Session = Depends(get_db)):
    db_user = models.User(name=user.name)
    db.add(db_user)
    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=400, detail="User already exists")
    db.refresh(db_user)
    return as_dict(db_user)


@app.post("/user/{user_id}/account/")
def create_user_account(*, user_id: int, account: Account, db: Session = Depends(get_db)):
    db_account = models.Account(name=account.name, user_id=user_id)
    db.add(db_account)
    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=400, detail="Account already exists")
    db.refresh(db_account)
    return as_dict(db_account)


@app.post("/user/{user_id}/address/")
def create_user_address(*, user_id: int, address: Address, db: Session = Depends(get_db)):
    db_address = models.Address(name=address.name, content=address.content)
    db.add(db_address)

    try:
        db.commit()
        db.refresh(db_address)
        db_user_address_mapping = models.UserAddressMapping(user_id=user_id, address_id=db_address.id)
        db.add(db_user_address_mapping)
        db.commit()

    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=400, detail="Address already exists")
    db.refresh(db_address)
    return as_dict(db_address)


@app.post("/user/{user_id}/assign_address/{address_id}/")
def assign_user_address(*, user_id: int, address_id: int, db: Session = Depends(get_db)):
    db_user_address_mapping = models.UserAddressMapping(user_id=user_id, address_id=address_id)
    (db.query(models.UserAddressMapping)
        .filter(models.UserAddressMapping.user_id == user_id, models.UserAddressMapping.address_id == address_id)
        .delete())
    db.add(db_user_address_mapping)
    try:
        db.commit()
    except sqlalchemy.exc.IntegrityError:
        logger.exception(f'Saving mapping error: {user_id} {address_id}')
        raise HTTPException(status_code=400, detail="Invalid mapping")
    db.refresh(db_user_address_mapping)
    return as_dict(db_user_address_mapping)
