from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint

from database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)


class Account(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), index=True)
    __table_args__ = (UniqueConstraint('user_id', 'name', name='_user_id_name_uc'),)


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    content = Column(String)


class UserAddressMapping(Base):
    __tablename__ = "user_address_mapping"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    address_id = Column(Integer, ForeignKey("address.id"))
    __table_args__ = (UniqueConstraint('user_id', 'address_id', name='_user_id_address_id_uc'),)
