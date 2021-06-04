from sqlalchemy.orm import registry, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine

mapper_registry = registry()
print(mapper_registry.metadata)

Base = mapper_registry.generate_base()

class User(Base):
    __tablename__ = 'user_account'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    full_name = Column(String)
    addresses = relationship('Address', back_populates='user')

    def __repr__(self) -> str:
        return f'User(id={self.id!r}, name={self.name!r}, fullname={self.full_name!r})'

class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user_account.id'))
    user = relationship('User', back_populates='addresses')

print('-' * 15)

print(User.__table__)
print(Address.__table__)

print('-' * 15)

engine = create_engine('sqlite+pysqlite:///:memory:', echo=True, future=True)

mapper_registry.metadata.create_all(engine)

print('-' * 15)

Base.metadata.create_all(engine)

print('-' * 15)

sandy = User(name='sandy', full_name='Sandy Cheeks')
print(sandy)