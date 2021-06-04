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

# read
with SessionLocal() as db:
    sandy = db.query(User).filter(User.id == 1).first()
    print(sandy)

with SessionLocal() as db:
    stmt = select(User).filter_by(id=1)
    sandy = db.execute(stmt).scalar_one()
    print(sandy)

with SessionLocal() as db:
    stmt = select(User).where(User.id == 1)
    sandy = db.execute(stmt).scalar_one()
    print(sandy)

with SessionLocal() as db:
    sandy = db.get(User, 1)
    print(sandy)

# update
with SessionLocal() as db:
    sandy = db.query(User).filter(User.id == 1).first()
    
    sandy.age = 27
    print(f'sandy in db.dirty? {sandy in db.dirty}')

    db.commit()
    print(f'sandy in db.dirty? {sandy in db.dirty}')

    sandy = db.query(User).filter(User.id == 1).first()
    print(sandy)

# delete
with SessionLocal() as db:
    # create
    mark = User(name='mark', age=23)

    db.add(mark)
    db.commit()

    # delete
    mark = db.get(User, 2)
    
    db.delete(mark)
    db.commit()

    # read, check
    try:
        stmt = select(User).where(User.name == 'mark')
        mark = db.execute(stmt).scalar_one()
        print(mark)
    except NoResultFound as nrf:
        print(nrf)

with SessionLocal() as db:
    # create
    mark = User(name='mark', age=24)

    db.add(mark)
    db.commit()

    # delete
    stmt = delete(User).where(User.id == 3)
    db.execute(stmt)
    db.commit()

    # read, check
    try:
        stmt = select(User).where(User.name == 'mark')
        mark = db.execute(stmt).scalar_one()
        print(mark)
    except NoResultFound as nrf:
        print(nrf)
