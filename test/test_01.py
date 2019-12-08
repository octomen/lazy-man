import pytest
from sqlalchemy.orm import scoped_session, sessionmaker

from db.factory import Factory
from db.models import T1, T2, T3, T4, engine, Base


@pytest.fixture()
def session():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = scoped_session(sessionmaker(bind=engine))
    yield session
    session.close()
    Base.metadata.drop_all(engine)


def test_create_recursive(session):
    factory = Factory(engine, Base)
    t3 = factory.create_model(T3, session)
    assert t3
    t1 = session.query(T1).one()
    t2 = session.query(T2).one()
    assert not session.query(T4).count()

    assert t3.t2 == t2
    assert t2.t1 == t1


def test_column(session):
    factory = Factory(engine, Base)
    t3 = factory.create_model(T3, session, {T1.name: 'kek'})
    session.commit()
    assert t3.t2.t1.name == 'kek'


def test_object(session):
    factory = Factory(engine, Base)
    t1 = T1(name='lol', number=666)
    t3 = factory.create_model(T3, session, {T1: t1})
    session.commit()
    assert t3.t2.t1 == t1


def test_column_and_object(session):
    factory = Factory(engine, Base)
    t1 = T1(name='lol', number=666)
    t3 = factory.create_model(T3, session, {T2.name: 'kek', T1: t1})
    session.commit()
    assert t3.t2.name == 'kek'
    assert t3.t2.t1 == t1
