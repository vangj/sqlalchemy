from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine, select, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

    def __repr__(self) -> str:
        return f'User(id={self.id!r}, name={self.name!r}, age={self.age!r})'

engine = create_engine('sqlite+pysqlite:///:memory:', echo=True, future=True)
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)
Base.metadata.create_all(bind=engine)

# create
with SessionLocal() as db:
    sandy = User(name='sandy', age=23)

    db.add(sandy)
    db.commit()


# update
with SessionLocal() as db:
    (db
        .query(User)
        .filter(User.id == 1)
        .update({'age': 27}, synchronize_session='fetch'))
    db.commit()

with SessionLocal() as db:
    sandy = db.get(User, 1)
    print(sandy)
    print('-' * 15)
