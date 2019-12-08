import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.ext.declarative import declarative_base

# engine = sa.create_engine('sqlite://')
engine = sa.create_engine('postgres://postgres@localhost:5432/postgres')
Base = declarative_base()


class T4(Base):
    __tablename__ = 't4'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    number = sa.Column(sa.Integer)


class T1(Base):
    __tablename__ = 't1'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    number = sa.Column(sa.Integer)


class T2(Base):
    __tablename__ = 't2'

    id = sa.Column(sa.Integer, primary_key=True)

    t1_id = sa.Column(sa.Integer, sa.ForeignKey(T1.id), nullable=False)
    t4_id = sa.Column(sa.Integer, sa.ForeignKey(T4.id), nullable=True)
    name = sa.Column(sa.String, nullable=False)
    number = sa.Column(sa.Integer)

    t1 = so.relationship(T1)
    t4 = so.relationship(T4)


class T3(Base):
    __tablename__ = 't3'

    id = sa.Column(sa.Integer, primary_key=True)
    t2_id = sa.Column(sa.Integer, sa.ForeignKey(T2.id), nullable=False)
    name = sa.Column(sa.String, nullable=False)
    number = sa.Column(sa.Integer)

    t2 = so.relationship(T2)
