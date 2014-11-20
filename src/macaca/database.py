"""
File: database.py
Author: Rinat F Sabitov
Email: 0
Github: 0
Description:
"""


import sqlalchemy as sqla
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager


db = sqla.create_engine('sqlite:///macaca.sqlite')
Session = sessionmaker(bind=db)
Base = declarative_base()


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class MacacaDatabaseError(Exception):
    pass


class User(Base):
    __tablename__ = 'users'

    jid = sqla.Column(sqla.String, unique=True, primary_key=True)
    name = sqla.Column(sqla.String)
    fullname = sqla.Column(sqla.String)
    key = sqla.Column(sqla.String, unique=True)
    external_id = sqla.Column(sqla.Integer, unique=True)

    def __repr__(self):
        return "<User(jid='%s', fullname='%s')>" % (self.jid, self.fullname)

    @classmethod
    def get_user_by_jid(self, jid):
        return Session().query(User).filter(User.jid == jid).first()


def init_database():
    Base.metadata.create_all(db)


def drop_database():
    assert False
    Base.metadata.drop_all(db)

